## Project Overview

** This Project aims to develop a from scratch DNS Resolution library **

- **_user.py** offers simple human interaction and is very easy to use.

- **_get_results.py** offers command line testing environment.

- **controller.py** defined methods that creates dns query and resolves.


## Example Step by Step: DNS Resolution and DNS Tunneling

*** Example Step by Step on DNS Resolution and DNS Tunneling ***

1. A user types a domain name into a web browser.
    - Example: "example.com".
2. The user's request checks the computer cache. If found, the DNS resolution is retrieved using **dns_caches**.
3. If not found, the request is forwarded to the **DNS_Local_resolver**.
4. The **DNS_Local_resolver** checks its cache. If the record is not there, it queries the **DNS_ISP_resolver**.
5. The **DNS_ISP_resolver** uses the ISP-level cache for domain resolution. If unresolved, it forwards the request to the **DNS_Root_resolver**.
6. The **DNS_Root_resolver** identifies the Top-Level Domain (TLD) server, forwarding the request to the **DNS_TLD_resolver**.
7. The **DNS_TLD_resolver** maps the domain to its authoritative server, sending the query to the **DNS_Authoritative_resolver**.
8. The **DNS_Authoritative_resolver** provides the definitive answer based on its cache or configuration.
9. DNS Tunneling Integration:
    - Encoded queries are handled by the **DNS_safe_resolver**, which decodes and reconstructs the original domain name for resolution.
    - The reconstructed query follows the same hierarchical resolution process to ensure accurate results.

This process ensures flexibility for DNS resolution, making it suitable for testing, scalability, and secure DNS tunneling scenarios.

---

## Simplified DNS Resolution Example

1. A user types a domain name into a web browser.
    - Example: "example.com".
2. The user's request checks the computer cache. If found, the DNS resolution is retrieved.
3. If not found, the request is forwarded to the Local DNS Resolver.
4. The Local DNS Resolver checks its cache. If not found, it queries the ISP's DNS Resolver.
5. The ISP's DNS Resolver queries the Root DNS Server.
6. The Root DNS Server provides information about the appropriate Top-Level Domain (TLD) Server.
7. The request is sent to the TLD DNS Server, which forwards it to the Authoritative DNS Server.
8. The Authoritative DNS Server resolves the domain name to an IP address and sends the response back to the user.

---

## DNS Packet Structure

DNS packets consist of several sections that work together to facilitate domain name resolution. Here's a high-level overview of the structure:

1. **Header**:
    - Includes metadata such as transaction ID, flags, and the number of entries in each section (questions, answers, authority, and additional).
2. **Question Section**:
    - Contains the domain name being queried, query type (e.g., A, AAAA, MX), and query class (e.g., IN for Internet).
3. **Answer Section**:
    - Contains resource records that answer the query, including the domain name, record type, TTL, and resource data (e.g., IP address).
4. **Authority Section**:
    - Provides information about authoritative name servers for the domain, helping recursive resolvers find the answer.
5. **Additional Section**:
    - Includes additional helpful information, such as IP addresses of name servers mentioned in the authority section.

### Visual Representation of a DNS Packet Structure

```
+---------------------+
|        Header       |
+---------------------+
|      Question       |
+---------------------+
|       Answer        |
+---------------------+
|      Authority      |
+---------------------+
|     Additional      |
+---------------------+
```

#### Detailed Breakdown:

**Header:**
```
+--------------------------+
|       Transaction ID    |
+--------------------------+
|         Flags           |
+--------------------------+
| Number of Questions     |
+--------------------------+
| Number of Answer RRs    |
+--------------------------+
| Number of Authority RRs |
+--------------------------+
| Number of Additional RRs|
+--------------------------+
```
- Transaction ID: Unique ID to match requests and responses.
- Flags: Contains query/response indicator and other flags.
- Counts: Specifies the number of entries in each section.

**Question Section:**
```
+--------------------------+
|      Query Name         |
+--------------------------+
|      Query Type         |
+--------------------------+
|      Query Class        |
+--------------------------+
```
- Domain Name: The queried domain (e.g., "example.com").
- Query Type: Type of record requested (e.g., A, AAAA, MX).
- Query Class: Internet (IN).

**Answer Section:**
```
+--------------------------+
|        Name             |
+--------------------------+
|        Type             |
+--------------------------+
|         TTL             |
+--------------------------+
|     Resource Data       |
+--------------------------+
```
- Name: Domain name associated with the record.
- Type: Record type (e.g., A for IPv4, AAAA for IPv6).
- TTL: Time-to-live value for caching.
- Resource Data: Actual data (e.g., IP address).

**Authority Section:**
```
+--------------------------+
|        Name             |
+--------------------------+
|        Type             |
+--------------------------+
|         TTL             |
+--------------------------+
|     Resource Data       |
+--------------------------+
```
- Name: Domain name of the authoritative server.
- Type: Record type (e.g., NS for name server).
- TTL: Time-to-live value.
- Resource Data: Address of the authoritative name server.

**Additional Section:**
```
+--------------------------+
|        Name             |
+--------------------------+
|        Type             |
+--------------------------+
|         TTL             |
+--------------------------+
|     Resource Data       |
+--------------------------+
```
- Includes extra information, such as IP addresses of name servers.

**Header:**
- Transaction ID: Unique ID to match requests and responses.
- Flags: Contains query/response indicator and other flags.
- Counts: Specifies the number of entries in each section.

**Question Section:**
- Domain Name: The queried domain (e.g., "example.com").
- Query Type: Type of record requested (e.g., A, AAAA, MX).
- Query Class: Internet (IN).

**Answer Section:**
- Name: Domain name associated with the record.
- Type: Record type (e.g., A for IPv4, AAAA for IPv6).
- TTL: Time-to-live value for caching.
- Resource Data: Actual data (e.g., IP address).

**Authority Section:**
- Name: Domain name of the authoritative server.
- Type: Record type (e.g., NS for name server).
- TTL: Time-to-live value.
- Resource Data: Address of the authoritative name server.

**Additional Section:**
- Includes extra information, such as IP addresses of name servers.

---

DNS packets consist of several sections that work together to facilitate domain name resolution. It is important to understand packets for understanding DNS. Although, for use of this repo its not neccessary to understand every detail. 
For more detailed information on DNS packets, refer to additional resources.

---

## Additional Resources

*** Extra Information and Helpful Links ***

- **Helpful information on the DNS packet build:**
    [Project Primer on DNS Packets](https://mislove.org/teaching/cs4700/spring11/handouts/project1-primer.pdf)

- **Helpful on DNS Resolver, format, and interconnectivity:**
    [DNS Basics on Null Hardware](https://www.nullhardware.com/blog/dns-basics/)

- **Helpful base information for in-depth understanding on DNS resolution:**
    [GeeksforGeeks: Domain Name System (DNS) in Application Layer](https://www.geeksforgeeks.org/domain-name-system-dns-in-application-layer/)

- **Helpful base for the cache files:**
    [IANA root.cache file examples for base reference and understanding](https://www.iana.org/domains/root/files)
    
- **Helpful basic information on webserver set up and python files:**
    [Set up local dns server and webserver in python](https://hackernoon.com/how-to-set-up-a-local-dns-server-with-python)
