
# Environment & Physics #
SCREEN_SIZE: tuple[int, int] = (1200, 800)
FPS: int = 60

# Paddle #
PADDLE_OFFSET: int = 50
PADDLE_SIZE: tuple[int, int] = (150, 20)
INITIAL_PADDLE_POSITION: tuple[int, int] = (
    (SCREEN_SIZE[0]//2) - PADDLE_SIZE[0]//2,
    SCREEN_SIZE[1] - PADDLE_OFFSET
)
PADDLE_BORDER_RAD: int = 10

# Ball #
DEFAULT_BALL_RAD: int = 10
BALL_SPEED: int = 10

# Bricks #
NUM_OF_BRICKS: tuple[int, int] = (32, 30)
BRICK_SIZE: tuple[float, float] = (SCREEN_SIZE[0]/NUM_OF_BRICKS[0],
                                   (SCREEN_SIZE[1]*(3/4))/NUM_OF_BRICKS[1])
BRICK_BORDER_RAD: int = 5

# Files #
_RESOURCES_FP: str = "../Resources/"

LEVELS_FP: str = f"{_RESOURCES_FP}Levels/"
