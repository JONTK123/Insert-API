"""
Export module for converting generated data to various formats:
- SQL INSERT statements
- MongoDB insertMany commands
- CSV files
- JSON files
"""

import csv
import json
from typing import Any, Dict, List
from datetime import datetime, date
from pathlib import Path


def _serialize_value(value: Any) -> Any:
    """Convert Python values to serializable format."""
    if value is None:
        return None
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, (int, float, str, bool)):
        return value
    else:
        return str(value)


def _escape_sql_string(value: str) -> str:
    """Escape a string for SQL."""
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def export_to_sql(data: Dict[str, List[Dict[str, Any]]], 
                  table_name: str = None,
                  batch_size: int = 100) -> str:
    """
    Export generated data to SQL INSERT statements.
    
    Args:
        data: Dictionary mapping entity names to lists of records
        table_name: Optional table name (if only one entity)
        batch_size: Number of rows per INSERT statement
        
    Returns:
        SQL INSERT statements as a string
    """
    sql_commands = []
    sql_commands.append("-- Generated SQL INSERT statements")
    sql_commands.append("-- Generated at: " + datetime.now().isoformat())
    sql_commands.append("")
    
    entities = [table_name] if table_name and table_name in data else data.keys()
    
    for entity_name in entities:
        records = data[entity_name]
        
        if not records:
            sql_commands.append(f"-- No records for table: {entity_name}")
            sql_commands.append("")
            continue
        
        # Get column names from first record
        columns = list(records[0].keys())
        column_list = ", ".join(columns)
        
        sql_commands.append(f"-- Table: {entity_name} ({len(records)} records)")
        sql_commands.append("")
        
        # Generate INSERT statements in batches
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            values_list = []
            for record in batch:
                values = []
                for col in columns:
                    value = record.get(col)
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, bool):
                        values.append("TRUE" if value else "FALSE")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    elif isinstance(value, (datetime, date)):
                        values.append(_escape_sql_string(value.isoformat()))
                    else:
                        values.append(_escape_sql_string(str(value)))
                
                values_list.append("(" + ", ".join(values) + ")")
            
            insert_statement = f"INSERT INTO {entity_name} ({column_list}) VALUES\n"
            insert_statement += ",\n".join(values_list) + ";"
            sql_commands.append(insert_statement)
            sql_commands.append("")
    
    return "\n".join(sql_commands)


def export_to_mongodb(data: Dict[str, List[Dict[str, Any]]], 
                      collection_name: str = None) -> str:
    """
    Export generated data to MongoDB insertMany commands.
    
    Args:
        data: Dictionary mapping entity names to lists of records
        collection_name: Optional collection name (if only one entity)
        
    Returns:
        MongoDB JavaScript commands as a string
    """
    mongo_commands = []
    mongo_commands.append("// Generated MongoDB insertMany commands")
    mongo_commands.append("// Generated at: " + datetime.now().isoformat())
    mongo_commands.append("")
    
    entities = [collection_name] if collection_name and collection_name in data else data.keys()
    
    for entity_name in entities:
        records = data[entity_name]
        
        if not records:
            mongo_commands.append(f"// No records for collection: {entity_name}")
            mongo_commands.append("")
            continue
        
        mongo_commands.append(f"// Collection: {entity_name} ({len(records)} records)")
        mongo_commands.append("")
        
        # Convert records to JSON-serializable format
        serialized_records = []
        for record in records:
            serialized_record = {}
            for key, value in record.items():
                serialized_record[key] = _serialize_value(value)
            serialized_records.append(serialized_record)
        
        # Generate insertMany command
        records_json = json.dumps(serialized_records, indent=2, ensure_ascii=False)
        
        mongo_commands.append(f"db.{entity_name}.insertMany(")
        mongo_commands.append(records_json)
        mongo_commands.append(");")
        mongo_commands.append("")
    
    return "\n".join(mongo_commands)


def export_to_csv(data: Dict[str, List[Dict[str, Any]]], 
                  output_dir: str = ".",
                  entity_name: str = None) -> Dict[str, str]:
    """
    Export generated data to CSV files.
    
    Args:
        data: Dictionary mapping entity names to lists of records
        output_dir: Directory to save CSV files
        entity_name: Optional entity name (if only one entity)
        
    Returns:
        Dictionary mapping entity names to file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_paths = {}
    entities = [entity_name] if entity_name and entity_name in data else data.keys()
    
    for entity_name in entities:
        records = data[entity_name]
        
        if not records:
            continue
        
        # Get column names from first record
        columns = list(records[0].keys())
        
        # Create CSV file
        csv_file = output_path / f"{entity_name}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            
            for record in records:
                # Serialize values for CSV
                csv_record = {}
                for key, value in record.items():
                    csv_record[key] = _serialize_value(value)
                writer.writerow(csv_record)
        
        file_paths[entity_name] = str(csv_file)
    
    return file_paths


def export_to_json(data: Dict[str, List[Dict[str, Any]]], 
                   output_dir: str = ".",
                   entity_name: str = None,
                   single_file: bool = False) -> Dict[str, str]:
    """
    Export generated data to JSON files.
    
    Args:
        data: Dictionary mapping entity names to lists of records
        output_dir: Directory to save JSON files
        entity_name: Optional entity name (if only one entity)
        single_file: If True, export all entities to a single file
        
    Returns:
        Dictionary mapping entity names to file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_paths = {}
    
    if single_file:
        # Export all data to a single JSON file
        serialized_data = {}
        for ent_name, records in data.items():
            serialized_records = []
            for record in records:
                serialized_record = {k: _serialize_value(v) for k, v in record.items()}
                serialized_records.append(serialized_record)
            serialized_data[ent_name] = serialized_records
        
        json_file = output_path / "all_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(serialized_data, f, indent=2, ensure_ascii=False)
        
        file_paths["all"] = str(json_file)
    else:
        # Export each entity to a separate JSON file
        entities = [entity_name] if entity_name and entity_name in data else data.keys()
        
        for ent_name in entities:
            records = data[ent_name]
            
            if not records:
                continue
            
            # Serialize records
            serialized_records = []
            for record in records:
                serialized_record = {k: _serialize_value(v) for k, v in record.items()}
                serialized_records.append(serialized_record)
            
            # Create JSON file
            json_file = output_path / f"{ent_name}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(serialized_records, f, indent=2, ensure_ascii=False)
            
            file_paths[ent_name] = str(json_file)
    
    return file_paths


def export_all(data: Dict[str, List[Dict[str, Any]]], 
               output_dir: str = ".",
               formats: List[str] = None) -> Dict[str, Any]:
    """
    Export data to multiple formats at once.
    
    Args:
        data: Dictionary mapping entity names to lists of records
        output_dir: Directory to save files
        formats: List of formats to export (sql, mongodb, csv, json). Default: all
        
    Returns:
        Dictionary with export results for each format
    """
    if formats is None:
        formats = ["sql", "mongodb", "csv", "json"]
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    if "sql" in formats:
        sql_file = Path(output_dir) / "insert_commands.sql"
        sql_commands = export_to_sql(data)
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(sql_commands)
        results["sql"] = str(sql_file)
    
    if "mongodb" in formats:
        mongo_file = Path(output_dir) / "insert_commands.js"
        mongo_commands = export_to_mongodb(data)
        with open(mongo_file, 'w', encoding='utf-8') as f:
            f.write(mongo_commands)
        results["mongodb"] = str(mongo_file)
    
    if "csv" in formats:
        csv_files = export_to_csv(data, output_dir)
        results["csv"] = csv_files
    
    if "json" in formats:
        json_files = export_to_json(data, output_dir)
        results["json"] = json_files
    
    return results
