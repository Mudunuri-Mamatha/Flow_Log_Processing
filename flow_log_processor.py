# Protocol number to name mapping
PROTOCOL_MAP = {
    "6": "tcp",
    "17": "udp",
    "1": "icmp"
}

def load_lookup_table(lookup_file):
    """Load the lookup table into a regular dictionary."""
    lookup_dict = {}  # Regular dictionary to store (dstport, protocol) -> tags

    with open(lookup_file, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue  # Skip malformed lines
            
            dstport, protocol, tag = parts[0].strip(), parts[1].strip().lower(), parts[2].strip()
            key = (dstport, protocol)

            # Add the tag to the dictionary
            if key in lookup_dict:
                lookup_dict[key].append(tag)
            else:
                lookup_dict[key] = [tag]

    return lookup_dict

def process_flow_logs(flow_file, lookup_dict):
    """Process flow logs and map each log to a tag."""
    tag_counts = {}  # Regular dictionary for tag counts
    port_protocol_counts = {}  # Regular dictionary for port/protocol counts

    with open(flow_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 14:
                continue  # Skip malformed lines

            dstport = parts[6]
            protocol_num = parts[7]
            protocol = PROTOCOL_MAP.get(protocol_num, "unknown").lower()

            # Lookup tags
            tags = lookup_dict.get((dstport, protocol), ["Untagged"])
            for tag in tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1

            # Update port/protocol counts
            key = (dstport, protocol)
            if key in port_protocol_counts:
                port_protocol_counts[key] += 1
            else:
                port_protocol_counts[key] = 1

    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    """Write the processed counts to an output file with sorting."""
    with open(output_file, 'w') as file:
        # Write Tag Counts (sorted by count in descending order)
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags:
            file.write(f"{tag},{count}\n")

        # Write Port/Protocol Combination Counts (default order)
        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    # Update paths as needed
    lookup_file = "./lookup.csv"
    flow_file = "./flow_logs.txt"
    output_file = "./output.txt"

    lookup_dict = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = process_flow_logs(flow_file, lookup_dict)
    write_output(tag_counts, port_protocol_counts, output_file)

if __name__ == "__main__":
    main()
