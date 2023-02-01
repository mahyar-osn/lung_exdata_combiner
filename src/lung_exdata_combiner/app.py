import os
from pathlib import Path
import argparse

from combiner import read_single_group, write_ex
from group_points import Point

GROUPS = {'edge_RL_base_lat': 'lateral edge of base of lower lobe of right lung',
          'edge_RL_base_med': 'medial edge of base of lower lobe of right lung',
          'edge_RL_fiss_base': 'base edge of oblique fissure',
          'edge_RL_H_fiss_lat': 'lateral edge of horizontal fissure of lower lobe of right lung',
          'edge_RL_H_fiss_med': 'medial edge of horizontal fissure of lower lobe of right lung',
          'edge_RL_posterior': 'posterior edge of lower lobe of right lung',
          'edge_RM_anterior': 'anterior edge of middle lobe of right lung',
          'edge_RM_base_lat': 'lateral edge of base of middle lobe of right lung',
          'edge_RM_base_med': 'medial edge of base of middle lobe of right lung',
          'edge_RM_H_fiss_lat': 'lateral edge of horizontal fissure of middle lobe of right lung',
          'edge_RM_H_fiss_med': 'medial edge of horizontal fissure of middle lobe of right lung',
          'edge_RM_O_fiss_lat': 'lateral edge of oblique fissure of middle lobe of right lung',
          'edge_RM_O_fiss_med': 'medial edge of oblique fissure of middle lobe of right lung',
          'edge_RU_ant_post': 'root of pulmonary valve',
          'RL_horiz_fissure': 'oblique fissure of upper lobe of right lung',
          'RLL_base': 'base of lower lobe of right lung surface',
          'RLL_lateral': 'lateral surface of lower lobe of right lung',
          'RLL_medial': 'medial surface of lower lobe of right lung',
          'RM_horiz_fissure': 'horizontal fissure of right lung',
          'RM_oblique_fissure': 'oblique fissure of middle lobe of right lung',
          'RML_base': 'base of middle lobe of right lung surface',
          'RML_lateral': 'lateral surface of middle lobe of right lung',
          'RML_medial': 'medial surface of middle lobe of right lung',
          'RUL_lateral': 'lateral surface of upper lobe of right lung',
          'RUL_medial': 'medial surface of upper lobe of right lung'}


class ProgramArguments(object):
    def __init__(self):
        self.input_ex_files = None
        self.output_ex_file = None


def main():
    args = parse_args()
    single_data = dict()
    if os.path.exists(args.input_ex_files):
        input_path = Path(args.input_ex_files)
        for ex_file in input_path.glob("*.exdata"):
            points = list()
            file_name = ex_file.stem
            if file_name in GROUPS.keys():
                group_name = GROUPS[file_name]
                data = read_single_group(str(ex_file))
                for p in data:
                    points.append(_create_point(p))
                single_data[group_name] = points

        if args.output_ex_file is None:
            output_ex = os.path.join(args.input_ex_files, 'combined_lung_data.ex')
        else:
            output_ex = args.output_ex_file

        write_ex(output_ex, single_data)


def _create_point(pts):
    return Point(float(pts[0]),
                 float(pts[1]),
                 float(pts[2]))


def parse_args():
    parser = argparse.ArgumentParser(description="Compile single lung exdata files into one combined exdata.")
    parser.add_argument("input_ex_files", help="Location (path) of the input exdata files.")
    parser.add_argument("--output_ex_file", help="Location (path) of the output ex file. "
                                                 "[defaults to the location of the input file if not set.]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == "__main__":
    main()
