from scrapinghub import ScrapinghubClient
import sys
def ApiError(apikey, project_id):
    client = ScrapinghubClient(apikey)
    project = client.get_project(project_id)
    spiders = project.spiders
    spider_list = spiders.list()
    error_matrix = {"include": []}
    item_matrix = {"include": []}
    for spider in spider_list:
        name = spider['id']
        store = spiders.get(name)
        jobs = store.jobs
        jobs_list = jobs.list()
        new_job_key = jobs_list[0]['key']
        new_job = project.jobs.get(new_job_key)
        error_logs = new_job.logs.list(level='ERROR')
        if error_logs:
            message = ''
            for log in error_logs:
                message = message + ' ' + log['message'] 
            error_matrix["include"].append({'spider':name, 'message':message})
        else:
            try:
                num_items_new_job = jobs_list[0]['items']
                
            except:
                item_matrix["include"].append({'spider':name, 'message':'has no items'})
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
                    item_matrix["include"].append({'spider':name, 'message':'The number of items returned has changed. Please investigate'})
                else:
                    continue
            else:
                continue
                
                
    return error_matrix, item_matrix

if __name__ == "__main__":
    ApiError(sys.argv[1], sys.argv[2])
