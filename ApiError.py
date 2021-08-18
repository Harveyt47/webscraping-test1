from scrapinghub import ScrapinghubClient
import sys
def ApiError(apikey, project_id):
    client = ScrapinghubClient(apikey)
    project = client.get_project(project_id)
    spiders = project.spiders
    spider_list = spiders.list()
    matrix = {"include": []}
    for spider in spider_list:
        name = spider['id']
        store = spiders.get(name)
        jobs = store.jobs
        jobs_list = jobs.list()
        job_key = jobs_list[0]['key']
        job = project.jobs.get(job_key)
        error_logs = job.logs.list(level='ERROR')
        if error_logs:
            message = ''
            for log in error_logs:
                message = message + ' ' + log['message'] 
            matrix["include"].append({'spider':name, 'message':message})
    print(matrix)    
    return matrix

if __name__ == "__main__":
    ApiError(sys.argv[1], sys.argv[2])
