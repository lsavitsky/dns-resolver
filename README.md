# README

## Purpose

Welcome to this GitHub repository! This repository is a comprehensive collection of tools, scripts, and classes for various networking, validation, and web server simulation tasks. It is designed to support developers and enthusiasts exploring custom exception handling, DNS server functionalities, and mock web servers.

This README provides an overview of the repository structure, descriptions of key files and folders, and a file path chart to help you navigate through the project efficiently.

---

## Quick Start

For a detailed overview of the project, including its objectives, DNS resolution steps, and packet structure, please visit the [Overview Document](./Overview.md).

---

## Repository Structure

### Root Directory

The root of the repository includes this README file and other high-level documentation or configuration files. Additionally, it contains two important Python files:

- **webserver.py**: Implements a basic web server, designed to serve HTML files and handle basic HTTP requests for testing or demonstration purposes.
- **user.py**: Emulates client interaction, acting as the entry point for user interaction and orchestrating calls to other parts of the repository, including DNS resolvers and the web server.

### Folders

- **validation/**
  - Contains custom exception classes designed to handle specific error scenarios.
- **html\_files/**
  - Includes basic HTML files for mock web server testing and experimentation.
- **dns\_servers/**
  - Hosts classes and utilities for DNS server operations.
  - Subfolders:
    - **tunneling/**
      - Placeholder for tunneling-related functionalities.
    - **dns\_construction/**
      - Contains tools and scripts used in constructing DNS packets or structures.
  - **dns\_caches/**
    - Includes example cache files for ISP, local, root, and safe resolvers, providing a starting point for testing and debugging DNS resolution. These caches are easily editable and scalable for adding more resolvers or domain mappings.
    - Subfolders:
      - **old\_mapping/**
        - Contains IP address mappings and additional cache files specific to outdated or legacy DNS mappings.
      - **auth\_mappings/**
        - Contains IP address mappings and authoritative DNS caches for specific domains or zones.

---

## File Descriptions

### validation/

- **InvalidCacheLineError.py**

  - A custom exception class to handle errors related to invalid cache lines. Useful in scenarios where data corruption or inconsistency is detected in cache operations.

- **InvalidRecordTypeError.py**

  - A custom exception class to handle invalid record type errors. Commonly used in contexts involving record validation or format mismatches.

### html\_files/

- **a.html**

  - A basic HTML file for mock web server testing.

- **b.html**

  - Another basic HTML file, similar in structure to `a.html`, primarily used for testing or demonstration purposes.

- **red panda.html**

  - A basic HTML file with the same structure as others but differentiated by its name.

### dns\_servers/

#### Root Directory

- **DNS\_ISP\_resolver.py**

  - Implements an ISP-level DNS resolver that uses a cache for faster resolution and falls back to the main resolver when necessary.

- **DNS\_local\_resolver.py**

  - Provides a local DNS resolver that prioritizes a local cache for domain resolution, with fallback to an ISP resolver.

- **DNS\_Recursive\_resolver.py**

  - A recursive DNS resolver that integrates multiple levels of resolvers:

    - **Local Resolver**: Queries a local DNS cache.
    - **ISP Resolver**: Utilizes an ISP-level cache for domain resolution.
    - **Root Resolver**: Retrieves TLD server information from a root cache.
    - **TLD Resolver**: Maps domains to their respective authoritative servers based on TLD.
    - **Authoritative Resolver**: Handles authoritative DNS resolution for specific zones.

  - The interaction hierarchy:

    1. Queries begin at the **Local Resolver**, which checks the local cache.
    2. If unresolved, the query proceeds to the **ISP Resolver**.
    3. Failing ISP resolution, it queries the **Root Resolver** for TLD information.
    4. The **TLD Resolver** identifies the authoritative server for the domain.
    5. Finally, the **Authoritative Resolver** provides the definitive answer for the query.

  - This layered approach ensures comprehensive and efficient DNS resolution, starting from the most specific cache and escalating to broader scopes as necessary.

  - A recursive DNS resolver that integrates local, ISP, root, TLD, and authoritative resolvers for complete domain resolution.

- **DNS\_resolver.py**

  - Base class for DNS resolvers, defining core functionalities like reading DNS cache files and handling resolutions.

- **DNS\_root.py**

  - A root DNS resolver that retrieves TLD server information and resolves domains to the appropriate TLD servers.

- **DNS\_safe\_resolver.py**

  - An extension of the recursive resolver, designed to securely decode DNS tunneling queries and enhance safety.
  - **Purpose**:
    - Provides additional mechanisms to handle encoded domain names, ensuring compatibility with DNS tunneling scenarios.
    - Focuses on decoding tunneled queries to extract the original domain name while maintaining secure resolution.
  - **DNS Tunneling Integration**:
    - The resolver identifies encoded domain names in queries.
    - Decodes the tunneled query to reconstruct the original domain.
    - Resolves the reconstructed domain name through the DNS hierarchy, ensuring accurate results even with tunneling techniques. An extension of the recursive resolver, adding safety mechanisms for encoded queries and secure cache handling.

- **DNS\_TLD\_resolver.py**

  - Defines the following key class:

    - **DNS\_TLD\_resolver**: Resolves domain names by interacting with TLD-specific caches based on root responses.
      - **Methods**:
        - `__init__(self, root_response: Enum)`: Initializes the TLD resolver using a root response and identifies the relevant TLD cache file.
        - `resolve(self) -> str`: Queries the TLD cache for a domain and returns the resolved IP address or `NXDOMAIN` if not found.

  - This file bridges the gap between root and authoritative DNS resolvers by handling domain resolution at the TLD level. A resolver for handling Top-Level Domain (TLD) queries, mapping domains to their respective authoritative servers.

- **DNS\_authoritative\_resolver.py**

  - Handles authoritative DNS resolution for specific zones based on TLD responses.

    - **Classes**:
      - **DNS\_Authoritative\_resolver**: Manages domain resolution within a specified authoritative zone.
        - **Methods**:
          - `__init__(self, dns_query: dns_packet, tld_response: Enum)`: Initializes the resolver using a DNS query and TLD response to determine the authoritative server.
          - `resolve(self) -> str`: Resolves the domain using the authoritative cache and returns the resolved IP address or `NXDOMAIN` if not found.

  - This file serves as the final step in the recursive resolution process, providing definitive answers based on authoritative data.

  - Handles authoritative DNS resolution for specific zones based on TLD responses.

### dns\_servers/dns\_construction/

- **dns\_packet.py**

  - Provides utilities for encoding and decoding DNS packets, including label-based encoding of domain names.

- **dns\_query\_flag.py**

  - Contains flag-related enums and methods used for constructing DNS query flags.

- **dns\_question\_enum.py**

  - Defines the following enumerations:
    - **QTYPE**: Represents DNS query types such as A (IPv4 address), AAAA (IPv6 address), MX (Mail exchange), and others.
    - **QCLASS**: Represents DNS query classes, including IN (Internet), CH (Chaos), and ANY (Wildcard query).
  - Provides utility methods for handling and validating these types, ensuring correct query formulation and decoding. Defines enumerations for DNS question types and classes, providing utility methods for handling and validating these types.

- **dns\_transaction\_and\_counts.py**

  - Implements transaction ID generation and counters for DNS sections, such as question, answer, authority, and additional sections.

- **DNS\_Tunnel\_enums.py**

  - Defines the following encoding schemes:
    - **Base16**: Encodes data using hexadecimal representation.
    - **Base32**: Encodes data using a 32-character set for compact representation.
    - **Base64**: Encodes data using a 64-character set, commonly used for encoding binary data in text format.
    - **Base85**: Encodes data using an 85-character set for higher efficiency.
    - **Base91**: Encodes data using a 91-character set for compact binary-to-text conversion.
    - **Binary**: Represents data in binary format with 8-bit segments.
    - **Hexadecimal**: Encodes data as hexadecimal characters.
    - **NetBios**: Placeholder for NetBios name encoding.
    - **DecimalEncoding**: Converts characters to their decimal ASCII values.
    - **ROT13**: Simple substitution cipher rotating characters by 13 places.
    - **URL**: Encodes data for safe use in URLs using percent encoding.
    - **ALL**: Applies all available encodings sequentially for testing purposes.
  - Each encoding scheme includes methods for:
    - **Encoding**: Converts input text to the respective encoded format.
    - **Decoding**: Reverts encoded data back to its original format.
  - Examples:
    - Base64 Encoding: Input `"hello"` -> Encoded `"aGVsbG8="`
    - ROT13 Encoding: Input `"hello"` -> Encoded `"uryyb"` Includes enums and methods for encoding and decoding data using various encoding schemes, such as Base64, Base32, and more, tailored for DNS tunneling scenarios.

- **dns\_answer\_enum.py**

  - Provides enums for DNS answer types and classes:

    - **ATYPE**: Defines DNS record types, including:

      - **A**: IPv4 address record.
      - **NS**: Name server record.
      - **CNAME**: Canonical name record.
      - **SOA**: Start of authority record.
      - **PTR**: Pointer record.
      - **MX**: Mail exchange record.
      - **TXT**: Text record.
      - **AAAA**: IPv6 address record.
      - **SRV**: Service location record.
      - **NULL**: Null resource record.
      - **ANY**: Wildcard for any record type.

    - **ACLASS**: Defines DNS record classes, including:

      - **IN**: Internet.
      - **CS**: CSNET (obsolete).
      - **CH**: Chaos.
      - **HESIOD**: Hesiod.
      - **NONE**: None.
      - **ANY**: Any class.

  - Includes utility methods for:

    - Retrieving names and values of record types.
    - Validating record types and classes. Provides enums for DNS answer types and classes, including utility methods for retrieving names and values of record types.

- **dns\_header\_construction.py**

  - Combines various components like transaction IDs, flags, and counters to construct the binary representation of DNS headers.

---

## File Path Chart

The full file path chart can be found in the [File Structure Document](./structure.md).

---

More files and descriptions will be added as the repository grows. Stay tuned for updates!

## Contribution

Feel free to contribute by opening issues or submitting pull requests. Your input helps improve and expand this repository.

