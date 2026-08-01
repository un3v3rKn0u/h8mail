#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `h8mail` package."""


import unittest
import tempfile
import os
import tarfile
import gzip # Unused import, but may be used if write_gzip_file function is uncommented
from h8mail.utils import run
from h8mail.utils import classes
from h8mail.utils import helpers
from h8mail.utils import localsearch
from h8mail.utils import localgzipsearch

def print_test_banner(testname):
    print("========================")
    print("========================")
    print("\tTESTING: "+testname)
    print("========================")
    print("========================")
    

class TestH8mail(unittest.TestCase):
    """Tests for `h8mail` package."""

    def write_text_file(self, filename, content):
        """Write content to a text file in temp_dir."""
        path = os.path.join(self.temp_path, filename)
        with open(path, "w", encoding="utf-8") as file_handle:
            file_handle.write(content)
        return path
    
    # Uncomment to test gzip writing functionality
    # def write_gzip_file(self, filename, content):
    #     """Write content to a gzip file in temp_dir."""
    #     path = os.path.join(self.temp_path, filename)
    #     with gzip.open(path, "wt", encoding="utf-8") as file_handle:
    #         file_handle.write(content)
    #     return path

    def setUp(self):
        """Generating local files with automatic cleanup (Python 3.10+)"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.temp_dir.name
        print(f"Created Temp Dir: {self.temp_path}")
        print(f"Registering dir + content for auto cleanup: {self.temp_path}")
        
        self.addCleanup(self.temp_dir.cleanup)


        # --- Dummy Data ---
        emails = """
        john.smith@gmail.com
        test@example.com
        fijsdhkfnhqsdkf
        fdqfqsdff
        test@evilcorp.com
        notfound@email.com
        """

        creds = """
        john.smith@gmail.com:SecretPASS
        bloblfd
        fjsdkf,ds
        test@evilcorp.com:An0therSECRETpassw0rd
        ddqsdqs
        """

        self.filetargets = self.write_text_file("test-emails.txt", emails)
        self.filetxt = self.write_text_file("test-creds.txt", creds)
                
        self.filegz = os.path.join(self.temp_path, "test-creds.tar.gz")
        with tarfile.open(self.filegz, "w:gz") as tar:
            tar.add(self.filetxt, arcname="test-creds.txt")
            
        print(f"Test files generated in : {self.temp_path}")


    @unittest.skipUnless(
        os.getenv("RUN_INTEGRATION_TEST") == "1",
        "Skipping integration test by default. Set RUN_INTEGRATION_TEST=1 to run."
    )
    def test_000_simple_integration_test(self):
        """Simple integration test"""
        run.print_banner()
        print_test_banner("VANILLA")

        user_args = run.parse_args(["-t", "test@example.com"])
        run.h8mail(user_args)

    def test_001_local_files_txt_gz(self):
        """Local file search Test"""
        run.print_banner()
        print_test_banner("TXT LOCAL")
        user_args_lb = run.parse_args(["-t", self.filetargets, "-lb", self.filetxt, "-sk"])
        run.h8mail(user_args_lb)
        print_test_banner("TXT LOCAL-SINGLFILE")
        user_args_lb = run.parse_args(["-t", self.filetargets, "-lb", self.filetxt, "-sk", "-sf"])
        run.h8mail(user_args_lb)

        run.print_banner()
        print_test_banner("GZ LOCAL")
        user_args_gz = run.parse_args(["-t", self.filetargets, "-gz", self.filegz, "-sk"])
        run.h8mail(user_args_gz)
        print_test_banner("GZ LOCAL-SINGLEFILE")
        user_args_gz = run.parse_args(["-t", self.filetargets, "-gz", self.filegz, "-sk", "-sf"])
        run.h8mail(user_args_gz)

    def test_002_parse_args_accepts_local_search_options(self) -> None:
        """Verify CLI argument parser correctly assigns local search flags."""
        arguments = run.parse_args(
            [
                "-t",
                "john.smith@gmail.com",
                "test@example.com",
                "-lb",
                "/tmp/synthetic-breach.txt",
                "-sk",
                "-sf",
            ]
        )

        self.assertEqual(
            arguments.user_targets,
            ["john.smith@gmail.com", "test@example.com"],
        )
        self.assertEqual(
            arguments.local_breach_src,
            ["/tmp/synthetic-breach.txt"],
        )
        self.assertTrue(arguments.skip_defaults)
        self.assertTrue(arguments.single_file)
        self.assertIsNone(arguments.user_urls)

    def test_003_parse_args_uses_safe_expected_defaults(self):
        """Verify CLI argument parser defaults to safe, expected values when given only a target."""
        arguments = run.parse_args(["-t", "john.smith@gmail.com"])
        self.assertFalse(arguments.skip_defaults)
        self.assertFalse(arguments.single_file)
        self.assertFalse(arguments.loose)
        self.assertFalse(arguments.debug)
        self.assertIsNone(arguments.output_file)
        self.assertIsNone(arguments.output_json)

    def test_005_url(self):
        run.print_banner()
        print_test_banner("URL-RAW")
        user_args_lb = run.parse_args(["-u", "https://raw.githubusercontent.com/khast3x/h8mail/master/tests/test_email.txt"])
        run.h8mail(user_args_lb)
        run.print_banner()
        print_test_banner("URL-MESSY")
        user_args_lb = run.parse_args(["-u", "https://raw.githubusercontent.com/khast3x/h8mail/master/tests/test_email.txt"])
        run.h8mail(user_args_lb)
