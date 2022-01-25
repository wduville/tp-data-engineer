import requests
import json
import pathlib

from tools import Timer

# 25-01-2022 - Issue:
# https://www.data.gouv.fr/api/1/datasets/?page=40001&page_size=1&sort=views


def fetch_all_datasets():
    page_size = 4000
    x_fields = 'total,page,next_page,previous_page,uri,page_size,data{id,title,slug,metrics,organization,page,description,tags}'

    result = run_query({'page': 0, 'page_size': 0}, headers={'X-Fields': 'total'})
    print("Total:", result['total'])
    # todo remove
    return

    with Timer("main"):
        for page in range(1, (result['total'] // 4000) + 1):
            with Timer(f"Page {page}"):
                result = run_query({'page': page, 'page_size': page_size}, headers={'X-Fields': x_fields})
                datasets = result['data']
                print(len(datasets), "items")

            filename = pathlib.Path(f'data/datasets_page_{page:02d}_size_{page_size}.json')
            filename.parent.mkdir(exist_ok=True)
            with filename.open('w') as f:
                json.dump(obj=result, fp=f, indent=2)

        print(len(datasets))


def run_query(params: dict = None, headers: dict = None, base_url: str = "https://www.data.gouv.fr/api/1/datasets/"):
    request = requests.get(url=base_url, params=params, headers=headers)
    if request.status_code == 200:
        return request.json()
    raise Exception(f"Query failed to run by returning code of {request.status_code}: {request.reason}. {params}")


if __name__ == '__main__':
    fetch_all_datasets()
