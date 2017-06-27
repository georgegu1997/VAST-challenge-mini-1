from classes import *

def write_in_json(data, file_name):
    with open(file_name, 'wb') as f:
        f.write(json.dumps(data, ensure_ascii=False))

def main():
    routes_data, gate_positions = read_all_data()

    Pattern.init_all_patterns()
    Pattern.sort_routes_into_pattern(Route.all_routes)
    write_in_json(Pattern.get_jsonable_all(), "patterns.json")

if __name__ == "__main__":
    main()
