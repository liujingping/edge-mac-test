#!/usr/bin/env python3
"""
Upload HTML failure analysis report to Azure Blob Storage and generate a SAS URL.

Usage:
    python scripts/upload_report.py --data-dir pipeline_data/141562849
    python scripts/upload_report.py --file reports/failure_analysis.html --build-id 141562849
"""

import argparse
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

AZURE_STORAGE_ACCOUNT_NAME = 'fsqtestreports'
AZURE_STORAGE_CONTAINER = 'reports'
SAS_EXPIRY_DAYS = 7


def get_storage_account_key(account_name: str) -> str:
    result = subprocess.run(
        [
            'az', 'storage', 'account', 'keys', 'list',
            '--account-name', account_name,
            '--query', '[0].value',
            '-o', 'tsv',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f'Failed to get storage account key. Run "az login" first.\n{result.stderr}'
        )
    return result.stdout.strip()


def ensure_container(account_name: str, account_key: str, container: str):
    subprocess.run(
        [
            'az', 'storage', 'container', 'create',
            '--name', container,
            '--account-name', account_name,
            '--account-key', account_key,
            '--public-access', 'off',
        ],
        capture_output=True,
        text=True,
    )


def upload_blob(
    account_name: str,
    account_key: str,
    container: str,
    blob_name: str,
    file_path: str,
) -> str:
    result = subprocess.run(
        [
            'az', 'storage', 'blob', 'upload',
            '--account-name', account_name,
            '--account-key', account_key,
            '--container-name', container,
            '--name', blob_name,
            '--file', file_path,
            '--content-type', 'text/html',
            '--overwrite',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f'Failed to upload blob.\n{result.stderr}')
    return blob_name


def generate_sas_url(
    account_name: str,
    account_key: str,
    container: str,
    blob_name: str,
    expiry_days: int = 7,
) -> str:
    expiry = (datetime.now(timezone.utc) + timedelta(days=expiry_days)).strftime(
        '%Y-%m-%dT%H:%MZ'
    )
    result = subprocess.run(
        [
            'az', 'storage', 'blob', 'generate-sas',
            '--account-name', account_name,
            '--account-key', account_key,
            '--container-name', container,
            '--name', blob_name,
            '--permissions', 'r',
            '--expiry', expiry,
            '--https-only',
            '--full-uri',
            '-o', 'tsv',
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f'Failed to generate SAS URL.\n{result.stderr}')
    return result.stdout.strip()


def upload_report(
    file_path: str,
    build_id: str,
    pipeline_name: str = '',
    account_name: str | None = None,
    container: str | None = None,
    expiry_days: int | None = None,
) -> str:
    account_name = account_name or AZURE_STORAGE_ACCOUNT_NAME
    container = container or AZURE_STORAGE_CONTAINER
    expiry_days = expiry_days or SAS_EXPIRY_DAYS

    if not Path(file_path).exists():
        raise FileNotFoundError(f'Report file not found: {file_path}')

    print('Uploading report to Azure Blob Storage...')
    print(f'  Account: {account_name}')
    print(f'  Container: {container}')

    account_key = get_storage_account_key(account_name)
    ensure_container(account_name, account_key, container)

    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H%M%S')
    safe_pipeline = pipeline_name.replace(' ', '_').replace('/', '_') if pipeline_name else 'unknown'
    blob_name = f'{safe_pipeline}/{build_id}/{date_str}_{time_str}_failure_analysis.html'

    upload_blob(account_name, account_key, container, blob_name, file_path)
    print(f'  Blob: {blob_name}')

    sas_url = generate_sas_url(
        account_name, account_key, container, blob_name, expiry_days
    )

    print(f'  SAS URL (expires in {expiry_days} days):')
    print(f'  {sas_url}')

    result = {'report_url': sas_url, 'build_id': build_id}
    result_file = Path(file_path).parent / 'report_url.json'
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f'  URL saved to: {result_file}')

    return sas_url


def main():
    parser = argparse.ArgumentParser(
        description='Upload HTML report to Azure Blob Storage'
    )
    parser.add_argument(
        '--data-dir',
        help='Pipeline data directory (e.g., pipeline_data/141562849)',
    )
    parser.add_argument('--file', help='Path to the HTML report file')
    parser.add_argument('--build-id', help='Build ID for blob naming')
    parser.add_argument('--account-name', help='Azure Storage account name')
    parser.add_argument('--container', help='Azure Storage container name')
    parser.add_argument(
        '--expiry-days', type=int, help='SAS URL expiry in days (default: 7)'
    )
    args = parser.parse_args()

    pipeline_name = ''
    if args.data_dir:
        data_dir = Path(args.data_dir)
        if not data_dir.is_absolute():
            data_dir = PROJECT_ROOT / data_dir
        report_file = str(data_dir / 'reports' / 'failure_analysis.html')
        pipeline_info_file = data_dir / 'pipeline_info.json'
        if pipeline_info_file.exists():
            with open(pipeline_info_file) as f:
                info = json.load(f)
            build_id = args.build_id or info.get('build_id', data_dir.name)
            pipeline_name = info.get('pipeline_name', '')
        else:
            build_id = args.build_id or data_dir.name
    elif args.file:
        report_file = args.file
        build_id = args.build_id or 'unknown'
    else:
        parser.error('Either --data-dir or --file is required')
        return

    upload_report(
        file_path=report_file,
        build_id=build_id,
        pipeline_name=pipeline_name,
        account_name=args.account_name,
        container=args.container,
        expiry_days=args.expiry_days,
    )


if __name__ == '__main__':
    main()
