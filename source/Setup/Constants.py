SCREEN_SIZE: tuple[int, int] = (1200, 800)

FPS: int = 60

PADDLE_OFFSET: int = 50
PADDLE_SIZE: tuple[int, int] = (100, 20)
INITIAL_PADDLE_POSITION: tuple[int, int] = (
    (SCREEN_SIZE[0]//2) - PADDLE_SIZE[0]//2,
    SCREEN_SIZE[1] - PADDLE_OFFSET
)
PADDLE_BORDER_RAD: int = 10

DEFAULT_BALL_RAD: int = 10
BALL_SPEED: int = 5
