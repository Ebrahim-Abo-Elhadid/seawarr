import numpy as np

from custtypes import Vec2


class Perlin2D:
    PERMUTATION_TABLE_SIZE = 256

    def __init__(self, seed: int | None = None):
        if seed is None:
            seed = np.random.randint(0, 2 ** 31)
        print(f"Using seed: {seed}")

        np.random.seed(seed)
        self.__random = np.random.default_rng(seed=seed)

        self.__permutation_table = [i for i in range(self.PERMUTATION_TABLE_SIZE)]
        np.random.shuffle(self.__permutation_table)
        self.__permutation_table = np.concatenate((self.__permutation_table, self.__permutation_table))

    @staticmethod
    def __normalizationSimple(x: float) -> float:
        return int(255 * abs(x))

    @staticmethod
    def __normalizationCustom(x: float, min_val: float, max_val: float) -> float:
        offset = -min_val
        if max_val + offset == 0:
            return 0
        return (x + offset) / (max_val + offset)

    @staticmethod
    def __fade(t: float):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def __interpolate(t: float, a: int, b: int):
        return a + t * (b - a)

    @staticmethod
    def __grad(hash: int, coords: Vec2):
        h = hash & 15
        u = coords[0] if h < 8 else coords[1]
        v = coords[1] if h < 4 else (coords[0] if h == 12 or h == 14 else 0)
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def __getPerlinAt(self, coords: Vec2) -> float:
        xi = int(coords[0]) & 255
        yi = int(coords[1]) & 255

        xf = coords[0] - int(coords[0])
        yf = coords[1] - int(coords[1])

        u = self.__fade(xf)
        v = self.__fade(yf)

        n00 = self.__grad(
            self.__permutation_table[self.__permutation_table[xi] + yi],
            (xf, yf))
        n01 = self.__grad(
            self.__permutation_table[self.__permutation_table[xi] + yi + 1],
            (xf, yf - 1))
        n10 = self.__grad(
            self.__permutation_table[self.__permutation_table[xi + 1] + yi],
            (xf - 1, yf))
        n11 = self.__grad(
            self.__permutation_table[self.__permutation_table[xi + 1] + yi + 1],
            (xf - 1, yf - 1))

        x1 = self.__interpolate(u, n00, n10)
        x2 = self.__interpolate(u, n01, n11)

        return self.__interpolate(v, x1, x2)

    @staticmethod
    def __getMaxAndMinValues(noise: list[list[float]]) -> tuple[float, float]:
        min_perlin = 10 ** 10
        max_perlin = -10 ** 10

        for i in noise:
            for j in i:
                if j > max_perlin:
                    max_perlin = j
                if j < min_perlin:
                    min_perlin = j

        return max_perlin, min_perlin

    @staticmethod
    def normalizeNoise(noise: np.array):
        max_val, min_val = Perlin2D.__getMaxAndMinValues(noise)

        for i in range(len(noise)):
            for j in range(len(noise[i])):
                color = Perlin2D.__normalizationCustom(noise[i][j], min_val, max_val)
                noise[i][j] = color

    def generatePerlin(self, size: Vec2, scale: float, octaves: int = 1) -> np.array:
        noise = np.ones(size)
        for octave in range(octaves):
            for i in range(size[0]):
                for j in range(size[1]):
                    x = i / scale
                    y = j / scale
                    p = self.__getPerlinAt((x, y))
                    noise[i][j] *= p

        self.normalizeNoise(noise)
        return noise

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    width, height = 256, 256
    scale = 32
    octaves = 1

    perlin = Perlin2D()

    noise = perlin.generatePerlin((width, height), scale, octaves)
    print(noise)

    plt.imshow(noise, cmap="gray")
    # plt.colorbar()
    plt.show()