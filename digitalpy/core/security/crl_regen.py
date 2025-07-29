#!/usr/bin/env python3
"""
Module: digitalpy.core.security.crl_regen
Description: Regenerate a Certificate Revocation List (CRL) and optionally append it to the CA bundle.
Version: 1.1.1
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class CertificateRevocationListController:
    def __init__(self, ca_pem_path: str, ca_key_path: str, crl_path: str, validity_days: int):
        """
        Controller for regenerating a Certificate Revocation List (CRL).

        Args:
            ca_pem_path: Path to the CA certificate PEM file
            ca_key_path: Path to the CA private key PEM file
            crl_path: Output path for the CRL (PEM or JSON)
            validity_days: Number of days until the next CRL update
        """
        self.ca_pem_path = ca_pem_path
        self.ca_key_path = ca_key_path
        self.crl_path = crl_path
        self.validity_days = validity_days

        # Load CA certificate
        with open(ca_pem_path, "rb") as f:
            self.ca_cert = x509.load_pem_x509_certificate(f.read())

        # Load CA private key (unencrypted PEM)
        with open(ca_key_path, "rb") as f:
            self.ca_key = load_pem_private_key(f.read(), password=None)

    def regenerate_crl(self):
        now = datetime.utcnow()
        next_update = now + timedelta(days=self.validity_days)

        # Build an empty CRL (add revoked certs here if needed)
        builder = (
            x509.CertificateRevocationListBuilder()
            .issuer_name(self.ca_cert.subject)
            .last_update(now)
            .next_update(next_update)
        )
        crl_obj = builder.sign(private_key=self.ca_key, algorithm=hashes.SHA256())

        # If JSON output requested
        if self.crl_path.lower().endswith(".json"):
            out = {
                "issuer": self.ca_cert.subject.rfc4514_string(),
                "last_update": now.isoformat() + "Z",
                "next_update": next_update.isoformat() + "Z",
                "revoked": [
                    {
                        "serial_number": rc.serial_number,
                        "revocation_date": rc.revocation_date.isoformat() + "Z",
                    }
                    for rc in crl_obj
                ],
            }
            with open(self.crl_path, "w") as f:
                json.dump(out, f, indent=2)
        else:
            # PEM output
            data = crl_obj.public_bytes(serialization.Encoding.PEM)
            with open(self.crl_path, "wb") as f:
                f.write(data)
            # Append to CA bundle
            with open(self.ca_pem_path, "ab") as f:
                f.write(data)

        # Print results
        print(f"✅ CRL regenerated: {self.crl_path}")
        print(f"  Last Update : {now.isoformat()}Z")
        print(f"  Next Update : {next_update.isoformat()}Z")


def main():
    # Header output
    print("digitalpy.core.security.crl_regen v1.1.0 - Regenerate a CRL and optionally append to the CA bundle.")

    parser = argparse.ArgumentParser(
        description="Regenerate a CRL and optionally append to your CA bundle."
    )
    parser.add_argument(
        "--ca-pem-path", required=True,
        help="Path to the CA certificate PEM file"
    )
    parser.add_argument(
        "--ca-key-path", required=True,
        help="Path to the CA private key PEM file"
    )
    parser.add_argument(
        "--crl-path", required=True,
        help="Output path for the CRL (supports .pem or .json extensions)"
    )
    parser.add_argument(
        "--validity-days", "--validity_days", type=int, default=365,
        dest="validity_days",
        help="Days until next_update (default: 365)"
    )

    args = parser.parse_args()

    try:
        ctl = CertificateRevocationListController(
            args.ca_pem_path,
            args.ca_key_path,
            args.crl_path,
            args.validity_days,
        )
        ctl.regenerate_crl()
    except Exception as e:
        print(f"❌ Error generating CRL: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
