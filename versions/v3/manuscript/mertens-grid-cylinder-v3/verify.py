import json
from fractions import Fraction
from itertools import product


def neighborhoods(rows, columns, wrap_rows=False, wrap_columns=False, king=False):
    masks = []
    for row, column in product(range(rows), range(columns)):
        adjacent = {(row, column)}
        steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if king:
            steps.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
        for row_step, column_step in steps:
            next_row = row + row_step
            next_column = column + column_step
            if wrap_rows:
                next_row %= rows
            if wrap_columns:
                next_column %= columns
            if 0 <= next_row < rows and 0 <= next_column < columns:
                adjacent.add((next_row, next_column))
        masks.append(sum(1 << (other_row * columns + other_column)
                         for other_row, other_column in adjacent))
    return masks


def dominating_subsets(masks):
    full = (1 << len(masks)) - 1
    coverage = [0] * (full + 1)
    dominating = set()
    for subset in range(1, full + 1):
        least_bit = subset & -subset
        coverage[subset] = coverage[subset ^ least_bit] | masks[least_bit.bit_length() - 1]
        if coverage[subset] == full:
            dominating.add(subset)
    if len(masks) <= 12:
        direct = {subset for subset in range(full + 1)
                  if all(subset & neighborhood for neighborhood in masks)}
        assert direct == dominating
    return dominating


def repair_pairs(dominating, target, boundary):
    pairs = set()
    for subset in dominating:
        repaired = subset | boundary
        assert repaired in target
        pair = repaired, subset & boundary
        assert pair not in pairs
        pairs.add(pair)
    return len(pairs)


def polynomial(dominating, vertices):
    coefficients = [0] * (vertices + 1)
    for subset in dominating:
        coefficients[subset.bit_count()] += 1
    return coefficients


def evaluate(coefficients, activity):
    return sum(coefficient * activity ** degree
               for degree, coefficient in enumerate(coefficients))


def extended_checks():
    activities = [Fraction(1, 2), Fraction(1), Fraction(2)]
    free_values = {}
    polynomials = []
    weighted_seams = 0
    weighted_torus_seams = 0
    king_repairs = 0
    for king in [False, True]:
        family = 'king' if king else 'cartesian'
        for rows, columns in product(range(1, 7), repeat=2):
            if rows * columns > 16:
                continue
            free = dominating_subsets(neighborhoods(rows, columns, king=king))
            coefficients = polynomial(free, rows * columns)
            free_values[family, rows, columns] = [evaluate(coefficients, activity)
                                                  for activity in activities]
            record = {'family': family, 'm': rows, 'n': columns,
                      'free_coefficients': coefficients}
            if rows >= 3:
                cylinder = dominating_subsets(neighborhoods(rows, columns, True, False, king))
                assert free <= cylinder
                cyclic_coefficients = polynomial(cylinder, rows * columns)
                record['cylinder_coefficients'] = cyclic_coefficients
                boundary = sum(1 << (row * columns + column)
                               for row in (0, rows - 1) for column in range(columns))
                if king:
                    king_repairs += repair_pairs(cylinder, free, boundary)
                for index, activity in enumerate(activities):
                    free_value = free_values[family, rows, columns][index]
                    cylinder_value = evaluate(cyclic_coefficients, activity)
                    assert free_value <= cylinder_value
                    assert cylinder_value <= (1 + 1 / activity) ** (2 * columns) * free_value
                    weighted_seams += 1
                if columns >= 3:
                    torus = dominating_subsets(neighborhoods(rows, columns, True, True, king))
                    assert cylinder <= torus
                    torus_coefficients = polynomial(torus, rows * columns)
                    record['torus_coefficients'] = torus_coefficients
                    boundary = sum(1 << (row * columns + column)
                                   for row in range(rows) for column in (0, columns - 1))
                    if king:
                        king_repairs += repair_pairs(torus, cylinder, boundary)
                    for activity in activities:
                        assert evaluate(torus_coefficients, activity) <= (
                            (1 + 1 / activity) ** (2 * rows)
                            * evaluate(cyclic_coefficients, activity))
                        weighted_torus_seams += 1
            polynomials.append(record)
    assert next(record['free_coefficients'] for record in polynomials
                if record['family'] == 'cartesian' and record['m'] == record['n'] == 3) == [
                    0, 0, 0, 10, 57, 98, 80, 36, 9, 1]
    assert next(record['free_coefficients'] for record in polynomials
                if record['family'] == 'king' and record['m'] == record['n'] == 2) == [
                    0, 4, 6, 4, 1]
    weighted_blocks = 0
    weighted_cuts = 0
    for (family, rows, columns), values in free_values.items():
        for (block_family, block_rows, block_columns), block_values in free_values.items():
            if family != block_family or block_rows > rows or block_columns > columns:
                continue
            row_blocks = rows // block_rows
            column_blocks = columns // block_columns
            blocks = row_blocks * column_blocks
            leftover = rows * columns - blocks * block_rows * block_columns
            for index, activity in enumerate(activities):
                assert block_values[index] ** blocks * activity ** leftover <= values[index]
                weighted_blocks += 1
                if rows % block_rows == 0 and columns % block_columns == 0:
                    boundary_bound = (2 * (row_blocks - 1) * columns
                                      + 2 * (column_blocks - 1) * rows)
                    assert values[index] <= (block_values[index] ** blocks
                                             * (1 + 1 / activity) ** boundary_bound)
                    weighted_cuts += 1
    return {
        'activities': [str(activity) for activity in activities],
        'arithmetic': 'Exact integers and fractions',
        'weighted_seam_inequalities': weighted_seams,
        'weighted_torus_seam_inequalities': weighted_torus_seams,
        'weighted_block_inequalities': weighted_blocks,
        'weighted_partition_upper_bounds': weighted_cuts,
        'king_repair_pairs': king_repairs,
        'polynomials': polynomials,
    }


def main():
    counts = {}
    cases = []
    seam_pairs = 0
    torus_pairs = 0
    seam_cases = 0
    torus_cases = 0
    for rows, columns in product(range(1, 7), repeat=2):
        if rows * columns > 16:
            continue
        grid = dominating_subsets(neighborhoods(rows, columns))
        counts[rows, columns] = len(grid)
        case = {'m': rows, 'n': columns, 'grid': len(grid)}
        if rows >= 3:
            cylinder = dominating_subsets(neighborhoods(rows, columns, wrap_rows=True))
            assert grid <= cylinder
            boundary = sum(1 << (row * columns + column)
                           for row in (0, rows - 1) for column in range(columns))
            seam_pairs += repair_pairs(cylinder, grid, boundary)
            assert len(cylinder) <= len(grid) * 4 ** columns
            seam_cases += 1
            case['cylinder'] = len(cylinder)
            if columns >= 3:
                torus = dominating_subsets(neighborhoods(rows, columns, True, True))
                assert cylinder <= torus
                boundary = sum(1 << (row * columns + column)
                               for row in range(rows) for column in (0, columns - 1))
                torus_pairs += repair_pairs(torus, cylinder, boundary)
                assert len(torus) <= len(cylinder) * 4 ** rows
                torus_cases += 1
                case['torus'] = len(torus)
        cases.append(case)
    assert counts[1, 1] == 1
    assert counts[2, 2] == 11
    assert counts[3, 3] == 291
    assert counts[4, 4] == 28661
    tilings = 0
    cut_bounds = 0
    for (rows, columns), total in counts.items():
        for (block_rows, block_columns), block_total in counts.items():
            if block_rows > rows or block_columns > columns:
                continue
            block_count = (rows // block_rows) * (columns // block_columns)
            assert block_total ** block_count <= total
            tilings += 1
            if rows % block_rows == 0 and columns % block_columns == 0:
                row_blocks = rows // block_rows
                column_blocks = columns // block_columns
                boundary_bound = (2 * (row_blocks - 1) * columns
                                  + 2 * (column_blocks - 1) * rows)
                assert total <= block_total ** block_count * 2 ** boundary_bound
                cut_bounds += 1
    result = {
        'coverage': 'Exact finite enumeration and combinatorial inequalities',
        'range': {'dimensions': '1 <= m,n <= 6', 'maximum_vertices': 16},
        'grid_cases': len(cases),
        'cylinder_cases': seam_cases,
        'torus_cases': torus_cases,
        'cylinder_repair_pairs': seam_pairs,
        'torus_repair_pairs': torus_pairs,
        'block_inequalities': tilings,
        'partition_upper_bounds': cut_bounds,
        'second_enumerator': 'Closed-neighborhood predicate for at most 12 vertices',
        'source_table': 'Mertens (2024), Table 8, square sizes 1 through 4',
        'cases': cases,
        'all_assertions': 'passed',
        'positive_activity_and_king_checks': extended_checks(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
