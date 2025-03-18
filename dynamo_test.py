import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")

# Select the tables
productos_table = dynamodb.Table('productos')
productos_duenio_table = dynamodb.Table('productos_duenio')


# ✅ Function to print all items from a table
def print_all_items(table, table_name):
    response = table.scan()  # Get all items
    items = response.get("Items", [])
    
    print(f"\n📌 Items in {table_name}:")
    for item in items:
        print(item)

    if not items:
        print(f"⚠️ No items found in {table_name}.")


print_all_items(productos_table, "productos")
print_all_items(productos_duenio_table, "productos_duenio")
