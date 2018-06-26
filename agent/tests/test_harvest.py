import json
import requests
import sys


def harvest_folder(source_dir, standard):
    output = {'success': False}

    data = {
        'source_dir': source_dir,
        'transport': 'FileSystem',
        'standard': standard,
        'upload_server_url': 'http://ckan.dirisa.org:9090/Institutions/webtide/sansa4/metadata',
        'upload_method': 'jsonCreateMetadataAsJson',
    }
    base = 'http://localhost:8080'
    url = "{}/harvest".format(base)
    print(url)
    response = requests.post(
        url=url,
        data=data,
    )
    if response.status_code != 200:
        output['error'] = 'Request failed with return code: %s' % (
            response.status_code)
        return output

    results = json.loads(response.text)
    output['results'] = results
    output['success'] = results['success']
    return output


if __name__ == "__main__":

    sources = [
        {
            'source_dir': '/home/mike/projects/harvester/data/Cbers MUX',
            'standard': 'CBERS_MUX'
        }, {
            'source_dir': '/home/mike/projects/harvester/data/Cbers P5M',
            'standard': 'CBERS_P5M'
        }, {
            'source_dir': '/home/mike/projects/harvester/data/SPOT6',
            'standard': 'SPOT6'
        }
    ]
    for source in sources:
        output = harvest_folder(source['source_dir'], source['standard'])

        if not output.get('success', False):
            print('Harvest failed, reason: {}'.format(results.get('error', 'unknown')))
            sys.exit()

        print('Harvest {}'.format(output['success']))
        results = output['results']
        for record in results['records']:
            if record['valid']:
                print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
            else:
                print('{title}: Valid = {valid}, Error = {error}, Upload = {upload_success} {upload_error}'.format(**record))
