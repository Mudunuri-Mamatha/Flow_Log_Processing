# Flow Log Processing Tool

## **Overview**

This program processes a flow log file and maps each row to a tag based on a lookup table. It generates an output file containing:

1. **Counts of matches for each tag**.
2. **Counts of matches for each `port/protocol` combination**.

The tool handles large files efficiently and requires minimal setup.

---

## **Prerequisites**

1. **Python 3.x** must be installed on your system.
2. Required files:
   - `lookup.csv`: The lookup table file with 3 columns: `dstport, protocol, tag`.
   - `flow_logs.txt`: The flow log file in plain text format.

---

## **Setup Instructions**

### **1. Clone or Download the Script**
Save the Python script to your working directory as `flow_log_processor.py`.

### **2. Prepare Input Files**
Ensure you download the following input files in the same directory:

#### **`lookup.csv`**
A CSV file with the following format:

```csv
dstport,protocol,tag
443,tcp,web
80,tcp,http
25,tcp,email
```

#### **`flow_logs.txt`**
A text file containing AWS VPC flow logs in the following format:

version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status

For example:

2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK


### **3. Place Files in the Same Directory**
Ensure the script, `lookup.csv`, and `flow_logs.txt` are in the **same directory**.

### **4. Install Python (if not installed)**
Download and install Python 3.x from [Python Official Website](https://www.python.org/downloads/).

---

## **How to Run the Program**

### **1. Open a Terminal or Command Prompt**
Navigate to the directory where the script and files are located.

### **2. Run the Script**
Execute the script with the following command:

```bash
python flow_log_processor.py
```

### **3. Check the Output**
The script generates an output file named `output.txt` in the same directory.

#### **Example contents of `output.txt`**:

Tag Counts:
Tag,Count
web,5
email,3
Untagged,10

Port/Protocol Combination Counts:
Port,Protocol,Count
443,tcp,3
80,tcp,2
25,tcp,5

---

## **Assumptions**

### **1. Flow Log Format**
- The flow log file follows **AWS VPC Flow Logs version 2 only**. Other versions are not supported.
- The expected column structure in the flow log file is:

version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status


- The **7th column (`dstport`)** and **8th column (`protocol`)** are used for tagging.

### **2. Protocol Mapping**
- The program only recognizes the following protocol numbers:
- `6` → **TCP**
- `17` → **UDP**
- `1` → **ICMP**
- Any other protocol numbers are labeled as `"unknown"`.

### **3. Lookup Table Format**
- The `lookup.csv` file must have exactly **3 columns**: `dstport, protocol, tag`.
- The first row is assumed to be a **header** and is skipped.
- If multiple tags exist for a `(dstport, protocol)` pair, all are stored and counted.
- **Case Insensitivity**: `tcp`, `TCP`, `udp`, `UDP` are treated the same.
- **Malformed rows** (fewer or more than 3 columns) are skipped.

### **4. Processing and Output Assumptions**
- If no tag is found for a `(dstport, protocol)`, it is labeled as `"Untagged"`.
- Tags are **sorted in descending order of frequency** in the output.
- The script assumes files are in **UTF-8 or ASCII format**.
- Malformed flow log entries with fewer than 14 columns are ignored.

### **5. Execution Environment**
- The script runs in any Python 3.x environment (Linux, Mac, Windows).
- It processes **large files up to 10MB efficiently**.

---

## **Troubleshooting**

### **1. FileNotFoundError**
- Ensure `lookup.csv` and `flow_logs.txt` are in the same directory as the script.
- If using absolute paths, update the script to use the correct file paths.

### **2. Lookup Table Issues**
- Ensure each row in `lookup.csv` has exactly **3 columns** (`dstport, protocol, tag`).
- Example of a valid row:

```csv
443,tcp,web
```

### **3. Flow Log Format Issues**
- Ensure each row in `flow_logs.txt` has **at least 14 columns**.
- Verify that `dstport` and `protocol` values match the lookup table format.

### **4. No Output or Empty Counts**
- Verify that `lookup.csv` and `flow_logs.txt` contain **matching** entries.
- Ensure that the protocol mapping in `PROTOCOL_MAP` correctly corresponds to your flow logs.

---

## **Contact**
For any questions or issues, ensure the lookup table and flow log files follow the expected formats and directory structure.

---


