#! /usr/bin/env python

# Example: ./scripts/request_curl.py --url http://localhost:3000/something --token abc --method GET
import argparse
import requests

def main():
  parser = argparse.ArgumentParser(description='Make request for the cron job')

  parser.add_argument('--url', required = True)
  parser.add_argument('--token', required = True)
  parser.add_argument('--method', required = True, choices = ['GET', 'POST'])
  args = parser.parse_args()

  headers = {
    'Authorization': f'Bearer {args.token}'
  }

  session = requests.Session()
  request = requests.Request(args.method,  args.url, headers = headers).prepare()
  response = session.send(request)

  print(response)

if __name__ == '__main__':
  main()
