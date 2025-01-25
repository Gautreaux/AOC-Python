from dataclasses import dataclass
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


_WHITE = "█"
_BLACK = " "
_UKN = "?"


@dataclass(frozen=True)
class ImageLayer:

    width: int
    height: int

    data: str


@dataclass(frozen=True)
class Image:

    width: int
    height: int
    layers: tuple[ImageLayer]

    @classmethod
    def from_byte_stream(
        cls, input_bytes: str, width: int = 25, height: int = 6
    ) -> "Image":
        """Parse and build an image from a stream of bytes"""

        layers = []

        bytes_per_layer = width * height

        assert len(input_bytes) % bytes_per_layer == 0
        assert len(input_bytes) > 0

        itr = iter(input_bytes)

        while True:
            this_layer_data = "".join(map(lambda _: next(itr), range(bytes_per_layer)))
            if this_layer_data:
                layers.append(
                    ImageLayer(
                        width=width,
                        height=height,
                        data=this_layer_data,
                    )
                )
            else:
                break

        return Image(width=width, height=height, layers=tuple(layers))

    def print(self):
        """Print this image to the console"""

        pixels = zip(*map(lambda x: x.data, self.layers))
        pixel_iter = iter(pixels)

        def get_pixel(this_pixel_over_layers: tuple[str]) -> str:
            for p in this_pixel_over_layers:
                if p == "0":
                    return _BLACK
                elif p == "1":
                    return _WHITE
            return _UKN

        for _ in range(self.height):
            for _ in range(self.width):
                print(get_pixel(next(pixel_iter)), end="")
            print("")  # newline


class Solution_2019_08(SolutionBase):
    """https://adventofcode.com/2019/day/8"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.image = Image.from_byte_stream(self.input_str().strip())

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        layer_with_least_zeros = min(self.image.layers, key=lambda l: l.data.count("0"))

        return layer_with_least_zeros.data.count(
            "1"
        ) * layer_with_least_zeros.data.count("2")

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        self.image.print()
        print("\nSee above output for image")
        return "YGRYZ"
