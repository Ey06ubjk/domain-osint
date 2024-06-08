# Semi-OSINT Automation

This Repo contains different files that completes the recon phase of a red team pentest according to MITRE ATT&CK (only 5 techniques),
because the other 5 techniques are part of a physical recon, which cannot be automated. 

To run the docker-container, it only needs the next prompts;

```
cd dockerPT2
```
```
docker-compose up --build
```

## OSINT Scanner Tool

The OSINT Scanner Tool is designed to enhance the efficiency and effectiveness of open-source intelligence (OSINT) gathering for companies. By leveraging five digital techniques aligned with the MITRE ATT&CK framework for reconnaissance, this tool speeds up the initial phase of risk analysis and client assessment.

## Basic Features
**Dns Records**: 
> This scan retrieves all DNS records associated with the domain, including A, AAAA, MX, TXT, and CNAME records. It provides insights into the domain’s configuration and can uncover associated domains or services.

**Workspace & Office 365 Usage Check**: 
> Identifies the utilization of Google Workspace and Microsoft Office 365 services by the domain. This information helps understand the collaboration tools the client uses, which can be pertinent in assessing their digital workflow and potential vulnerabilities.

**WHOIS Details**: 
> Fetches the registration details of the domain, such as the registrant’s name, organization, and contact information. This data is crucial for understanding the ownership and administrative control of the domain.

**Subdomains**: 
> Discovers all active subdomains of the primary domain. Mapping subdomains can reveal the extent of the client's web presence and potential areas susceptible to cyber attacks.

**WAF Check**: 
> Determines if a Web Application Firewall (WAF) protects the domain, which helps in evaluating the client’s frontline defense against web-based attacks.


## Advanced Scans
**Security-Headers Check**: 
> Evaluates the HTTP security headers used by the domain. These headers enforce security policies in web browsers, protecting users from various types of attacks like Cross-Site Scripting (XSS) and data injection.

**WordPress Scan (Active)**: 
> Performs an active scan on WordPress installations for vulnerabilities. This scan is essential for identifying unpatched security issues, outdated plugins, or configurations that could be exploited.

**Name and Title (Passive)**: 
> A passive scan that gathers names and titles associated with the domain or company from publicly available sources. This information is used to build a profile of key individuals in the organization, useful in both risk analysis and social engineering assessments.

**Emails and Format (Passive)**: 
> Collects email addresses and their formats associated with the domain. Understanding the email structure can help in identifying phishing risks and the spread of sensitive information.

**SSL Cert Check**: 
> Verifies the SSL certificate of a domain for validity and authenticity. It checks for proper issuance, expiration status, and encryption protocols to ensure secure and encrypted web communication. This scan is crucial for identifying vulnerabilities and ensuring compliance with security best practices.

**SSL/TLS Cert Check**: 
> Checks the validity and configuration of SSL/TLS certificates. This ensures that the domain's communications are encrypted and secure from interception or tampering.

**Open Ports (Active)**: 
> Scans for open TCP/UDP ports, identifying active services that could be exposed to the internet. This scan helps pinpoint potential vulnerabilities or unauthorized services running on the client’s network.

**System Uptime**: 
> Monitors and reports on the system uptime of servers associated with the domain. High uptime can indicate good system health, while frequent downtimes may suggest stability issues or maintenance challenges.

## Purpose

This tool is specifically tailored for companies that wish to conduct preliminary risk analyses and gather intelligence on potential or existing clients. By automating the collection of essential OSINT, the OSINT Scanner Tool aids in making informed decisions and directing strategic discussions based on data-driven insights.

### Getting Started

1. **Set Up**: Input the domain or company details into the appropriate fields.
2. **Select Scans**: Choose the scans you wish to perform from the comprehensive list of options.
3. **Run**: Execute the scans to collect data.
4. **Review**: Analyze the generated reports to guide your risk analysis discussions.
  
This tool not only streamlines the process of gathering open-source intelligence but also ensures that your engagements with clients are informed, strategic, and tailored to address specific security considerations.

## OSINT Tools
After completing the initial scans with the OSINT Scanner Tool, you can further enhance your open-source intelligence gathering by utilizing the "OSINT Tools" available in the navigation bar. This section provides access to a suite of online tools tailored for more detailed, manual OSINT tasks. These tools are designed to complement the automated scans, offering deeper insights and allowing for more precise data analysis and interpretation. Whether you need to cross-reference information, delve into social media analysis, or perform advanced data searches, the "OSINT Tools" section serves as a gateway to a broader range of resources for comprehensive intelligence gathering.

### Usage
1. **Access**: Click on the "OSINT Tools" tab in the navigation bar once your initial scans are complete.
2. **Selection**: Choose from a variety of online tools based on the specific needs of your investigation or analysis.
3. **Engage**: Utilize these tools to conduct thorough research, verify data, and gather additional information that can help in building a complete profile or assessing risks more accurately.

These tools are particularly useful for investigations that require a hands-on approach, providing the means to dig deeper into the data collected and explore specific aspects of a company’s or individual’s digital footprint.

> **Note**: Scan number 8 fails at first try, but works after. Work is in progress to solve the problem.
> Also this Proof of Concept is open for devolpment to add more scans. Enjoy!
