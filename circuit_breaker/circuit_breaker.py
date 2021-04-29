from enum import Enum
from datetime import datetime, timedelta


class States(Enum):
    CLOSED = 0
    OPENED = 1
    HALF_OPENED = 2


class CachedException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, service, timeout: int, retry_timeout: timedelta, failure_threshold: int):
        self._service = service
        self._state = States.CLOSED
        self._timeout = timeout
        self._retry_timeout = retry_timeout
        self._failure_threshold = failure_threshold

        self._last_failure_time = None
        self._last_failure_response = None
        self._failure_count = 0

    async def attempt_request(self, *args, **kwargs):
        await self.evaluate_state()
        if self._state == States.OPENED:
            return CachedException(
                self._last_failure_response,
                self._last_failure_time,
            )

        try:
            response = await self._service(timeout=self._timeout, *args, **kwargs)
            await self._response_success()
            return response
        except Exception as e:
            await self._response_failure(e)
            return e

    async def evaluate_state(self):
        if self._failure_count >= self._failure_threshold:
            if datetime.now() - self._last_failure_time > self._retry_timeout:
                self._state = States.HALF_OPENED
                self._failure_count //= 2
            else:
                self._state = States.OPENED
        else:
            self._state = States.CLOSED

    async def _response_success(self):
        self._state = States.CLOSED
        self._failure_count = 0
        self._last_failure_time = None

    async def _response_failure(self, response):
        self._state = States.OPENED
        self._failure_count += 1
        self._last_failure_time = datetime.now()
        self._last_failure_response = response

    async def get_state(self):
        return self._state

    async def set_state(self, state):
        self._state = state
        if state == States.OPENED:
            self._failure_count = self._failure_threshold
            self._last_failure_time = datetime.now()
        elif state == States.CLOSED:
            self._failure_count = 0
            self._last_failure_time = None
        elif state == States.HALF_OPENED:
            self._failure_count = self._failure_threshold // 2
            self._last_failure_time = datetime.now() - self._retry_timeout
