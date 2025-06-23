from dataclasses import dataclass

Vec2 = tuple[int | float, int | float]

@dataclass
class MouseState:
    is_clicked_left: bool
    is_clicked_right: bool
    position: Vec2
    last_left_click_time: float



if __name__ == "__main__":
    ms = MouseState(
        False, False, (0, 0), 0.0
    )
    ms.is_clicked_right = True

    print(ms)

    