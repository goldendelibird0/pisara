"""Run the whole pipeline: collect, line up, measure, group, publish.

    python pipeline/run.py [--accept-deped-terms]
"""
import sys

import s1_collect
import s2_lineup
import s3_measure
import s4_group
import s5_publish

if __name__ == "__main__":
    s1_collect.run("--accept-deped-terms" in sys.argv)
    s2_lineup.run()
    s3_measure.run()
    s4_group.run()
    s5_publish.run()
