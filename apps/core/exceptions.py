from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)


class DefaultException(Exception):
    detail: str | dict = "Algo de inesperado aconteceu. Entre em contato com suporte."
    code: int = HTTP_400_BAD_REQUEST
    internal_code: int = ''

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        detail = kwargs.get("detail", None)
        if detail:
            self.detail = detail
        code = kwargs.get("code", None)
        if code:
            self.code = code
        internal_code = kwargs.get("internal_code", None)
        self._set_internal_code(internal_code)

    def _set_internal_code(self, internal_code: int):
        if internal_code:
            if type(self.detail) is str:
                self.detail = f"{self.detail} [{internal_code}]"
            elif type(self.detail) is dict:
                self.detail["internal_error"] = f"{internal_code}"

    def __dict__(self):
        return {
            "detail": self.detail,
            "code": self.code,
            "internal_code": self.internal_code
        }

    def __str__(self):
        return self.detail


class ExceptDictTypeException(DefaultException):
    detail = "É esperado um dicionário."
    code = HTTP_401_UNAUTHORIZED
