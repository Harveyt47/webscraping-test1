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
        new_job_key = jobs_list[0]['key']
        new_job = project.jobs.get(new_job_key)
        error_logs = new_job.logs.list(level='ERROR')
        if error_logs:
            message = b''
            for log in error_logs:
                message = message + b' ' + log[b'message'] 
            matrix["include"].append({'spider':name, 'message':message, 'type':'ERROR'})
        else:
            try:
                num_items_new_job = jobs_list[0]['items']
                
            except:
                matrix["include"].append({'spider':name, 'message':'has no items', 'type':'ITEM'})
                continue
                
            # the loop below searchs for the first old job that has items
            num_items_old_job=0
            for job in jobs_list[1:]:
                try:
                    num_items_old_job = job['items']
                    old_job_key = job['key']
                    break
                except:
                    continue
            
            if num_items_old_job:
                if num_items_old_job != num_items_new_job:
                    matrix["include"].append({'spider':name, 'message':'The number of items returned has changed. Please investigate', 'type':'ITEM'})
                else:
                    continue
            else:
                continue
                
                
    return matrix

if __name__ == "__main__":
    ApiError(sys.argv[1], sys.argv[2])
