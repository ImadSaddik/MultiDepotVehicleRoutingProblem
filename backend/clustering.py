from typing import List

def assign_employees_to_buses(
    buses_data: List[tuple],
    employees_data: List[tuple],
    routes: List[dict],
    max_capacity: int = 18
) -> dict:
    assignments = {i: [] for i in range(len(buses_data))}
    unassigned_employees = set(range(len(employees_data)))

    for bus_idx, bus_location in enumerate(buses_data):
        if not unassigned_employees:
            break

        distances = {}
        for emp_idx in unassigned_employees:
            key = tuple(
                sorted((tuple(bus_location), tuple(employees_data[emp_idx]))))
            if key in routes:
                distances[emp_idx] = routes[key]['distance']
            else:
                distances[emp_idx] = float('inf')

        sorted_employee_indices = sorted(distances, key=distances.get)

        for emp_idx in sorted_employee_indices[:max_capacity]:
            if len(assignments[bus_idx]) < max_capacity:
                assignments[bus_idx].append(emp_idx)

        assigned = set(assignments[bus_idx])
        unassigned_employees -= assigned

    return assignments
