from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует",)
IncorrectEmail0rPasswordException = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль",)
TokenExpiredException = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек",)
TokenAbsentException = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует",)
IncorrentTokenFormatException = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена",)
UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
RoomCannotBeBooked = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Не осталось свободных номеров")