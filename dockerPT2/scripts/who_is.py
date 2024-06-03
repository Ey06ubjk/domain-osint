import whois, sys

# The domain to query, taken from the command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 whois.py <domain>")
    sys.exit(1)
domain = sys.argv[1]

def query_whois(domain):
    try:
        dm_info = whois.whois(domain)  # Get Domain Info using the whois module

        if dm_info.get('domain_name', 'null') == None:
            raise Exception

        print(f"domain_name: {dm_info.get('domain_name', 'null')}")
        print(f"dnssec: {dm_info.get('dnssec', 'null') if dm_info.get('dnssec') is not None else 'null'}\n")
        
        # Predefined order for printing certain fields before registrar_country, replacing None with 'null'
        predefined_order = ['updated_date', 'creation_date', 'status', 'registrar']
        
        # Print predefined fields
        for key in predefined_order:
            value = dm_info.get(key, 'null') if dm_info.get(key) is not None else 'null'
            print(f"{key}: {value}")
                
        print(f"expiration_date: {dm_info.get('expiration_date', 'null') if dm_info.get('expiration_date') is not None else 'null'}")
        print(f"registrar_country: {dm_info.get('registrar_country', 'null') if dm_info.get('registrar_country') is not None else 'null'}")
            
        # Handle name_servers, printing each server on its own line
        if 'name_servers' in dm_info:
            print("name_servers:")
            ns_list = dm_info.get('name_servers', [])
            if ns_list is None:  # Handle the case where ns_list is explicitly None
                print("  - null")
            elif isinstance(ns_list, list):
                for ns in ns_list:
                    print(f"  - {ns}")
            else:
                print(f"  - {ns_list}")
                
    except Exception as e:
        print("Whois script failed or Non-existent domain.")

if __name__ == "__main__":
    query_whois(domain)