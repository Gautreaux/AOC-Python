from collections import defaultdict
from dataclasses import dataclass
from AOC_Lib.Grid2d import Grid2d, Point2


@dataclass
class HikingTrailhead:
    
    start_point: Point2
    end_points: set[Point2]
    total_routes: int
    
    def get_score(self) -> int:
        return len(self.end_points)
    
    def get_rating(self) -> int:
        return self.total_routes


class HikingMap:
    
    def __init__(self, topological_map: Grid2d):
        self.topological_map: Grid2d = topological_map

        # A dict of height to points and their reachable end points
        self.height_caches: dict[int, dict[Point2, HikingTrailhead]] = {}
        
        # Pre seed the cache with the finish points
        self.height_caches[9] = {p:HikingTrailhead(p, {p}, 1) for p,_ in self.topological_map.generate_matching_points(9)}

    def get_height_map(self, layer: int) -> dict[Point2, HikingTrailhead]:
        assert layer >= 0
        assert layer <= 9

        if layer in self.height_caches:
            return self.height_caches[layer]
        
        prior_height_map = self.get_height_map(layer + 1)
        new_height_map: dict[Point2, HikingTrailhead] = {}

        height_filter = lambda v: v == layer

        for k,v in prior_height_map.items():
            # k - point in the prior layer that can reach an exit
            # v - all the reachable exits from that point

            for p, _ in self.topological_map.generate_neighbor_points(
                k, include_diagonals=False, value_filter=height_filter
            ):
                # p - a new point in the current layer
                #   that is nighbors to k
                if p in new_height_map:
                    new_height_map[p].end_points.update(v.end_points)
                    new_height_map[p].total_routes += v.total_routes
                else:
                    new_height_map[p] = HikingTrailhead(
                        start_point=p,
                        end_points=set(v.end_points),
                        total_routes=v.total_routes,
                    )
        
        self.height_caches[layer] = new_height_map
        return new_height_map

    def get_total_score(self, layer: int = 0) -> int:
        """Return the total score for the given layer"""
        height_map = self.get_height_map(layer)
        return sum(s.get_score() for s in height_map.values())

    def get_total_rating(self, layer: int = 0) -> int:
        """Return the total rating for the given layer"""
        height_map = self.get_height_map(layer)
        return sum(s.get_rating() for s in height_map.values())

def y2024d10(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d10.txt"
    print("2024 day 10:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    topo_map = Grid2d([list(map(int, p)) for p in lineList])
    hiking_map = HikingMap(topo_map)

    Part_1_Answer = hiking_map.get_total_score()
    Part_2_Answer = hiking_map.get_total_rating()

    return (Part_1_Answer, Part_2_Answer)