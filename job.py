#!/usr/bin/env python

'''
    I wanted to do something with AngelList's API
'''

import json
import settings as s
import sys
sys.path.append('/Users/Glove/Desktop/lob/angel-list/angel')
# the input should be creditals


import angel

al = angel.AngelList(s.CLIENT_ID, s.CLIENT_SECRET, s.ACCESS_TOKEN)
#print al

def pprint(input):
    print json.dumps(input)

def me(angel_h):
     user_info = {}
     skill_info = {}
     level_info = {}
     # only want to call the API once
     me_result = angel_h.get_self()

     # grab location info
     for loc in me_result['locations']:
     #for loc in angel_h.get_self()['locations']:
         user_info[loc['id']] = loc['display_name']

     # grab skill info
     for skill in me_result['skills']:
         skill_info[skill['id']] = skill['name']
         #skill_info[skill['id']]['level'] = '3' #skill['level']
     # TODO: build levels as nested dic/JSON

     # grab levels
     for level in me_result['skills']:
         level_info[level['id']] = level['level']

     return user_info, skill_info, level_info

#pprint(me(al))

user_info, skill_info, level_info = me(al)
#print skill_info.keys()
#sys.exit(33)

def pagination(method,id):

    results = []

    final_results = {}
    # TODO see note
    set_env =method(id)
    final_results = set_env
    last_page = set_env['last_page']
    current_page = 66    #needs to be set to to two
    job_results = {}

    #print job_results['last_page']
    # sys.exit(44)
    #last = job_results['last_page']

    #last_page = 1000000000
    #while job_results['page'] != 2: #page['last_page']:
    while current_page < last_page: #page['last_page']:
        #job_results = request.get_tag_jobs(id, page = num)
        job_results = method(id,page=current_page)
        last_page = job_results['last_page']
        '''for res in job_results['jobs']:
            print json.dumps(res['title'])
            results.append(res)
            #final_results[current_page] = res
            break
        '''
        #print json.dumps(job_results)
        #sys.exit(33)

        #break
        #print type(job_results)

        #print json.dumps(dict(job_results,**final_results))
        #jaren = {}
        #print json.dumps(final_results['jobs'])
        #print json.dumps(job_results['jobs'])
        output = final_results['jobs'] + job_results['jobs']
        final_results['jobs'] = output
        #print json.dumps(final_results)

        # jaren = final_results['jobs'].update(job_results['jobs'])
        #print json.dumps(jaren)
        #sys.exit(333)

        #final_results['jobs'].append(job_results)


        current_page = current_page + 1
        #print "------------------------------"
        #print results['jobs']['title']
        #print results['page']
    #print len(results)
    #final_results['jobs'] = results
    #return json.dumps(final_results)
    return final_results
    #return json.dumps(JAREN)


def job_search_by_location(angel_h,location_id,job_type):
    jobs_result = {}
    output =[]
    job_list = []
    api = angel_h.get_tag_jobs
    jobs = pagination(api,location_id)
    #print json.dumps(jobs)

    #sys.exit(555)
    #jobs = angel_h.get_tag_jobs(location_id)
    for job in jobs['jobs']:
        #print job['startup']['name']
        #if job['job_type'] == job_type and job[]
        for tag in job['tags']:
            #print tag['display_name']
            for skill_key in skill_info.keys():
                #print skill_key
                if tag['id'] == skill_key and job['job_type']== job_type and job['id'] not in jobs_result.keys()\
                        and job['startup']['quality'] > 6:  # remove quality
                   # print tag['display_name']
                    temp_job = {'title': job['title'],
                                'job': job['angellist_url'],
                                'job_id':job['id'],
                                'startup':job['startup']['name'],
                                'quality':job['startup']['quality'],
                                'salary_min':job['salary_min'],
                                'salary_max':job['salary_max'],
                                'equity_min':job['equity_min'],
                                'equity_max':job['equity_max'],
                                'startup_id':job['startup']['id'],
                                'equity_vest':job['equity_vest'],
                                'equity_cliff':job['equity_cliff'],
                                'currency_code':job['currency_code']}

                    #print "temp job type %s" % type(temp_job)
                    #print temp_job
                    #sys.exit(33)
                    #temp_job.extend([job['title'],job['angellist_url']])
                    #jobs_result[job['id']] = temp_job

                    output.append(temp_job)
                    jobs_result['job_id'] = output

                    #jobs_result['job_id'] = temp_job

                    #print temp_job
                    #if not tag['display_name'] in job_list: job_list.append(job)
                    #print json.dumps(job_list)
                    #sys.exit(333)
            #sys.exit(333)
    #print json.dumps(jobs_result)
    return jobs_result



def stats(jobs):
    output = []
    count = 0
    quality_total = 0
    startup_max = 0
    equity_cliff =0
    equity_vest = 0
    equity_max = 0
    #print json.dumps(jobs)
    #print
    #sys.exit(33)
    for job in jobs['job_id']:
        #print json.dumps(job)
        #sys.exit(33)
        #print json.dumps(job)
        #print type(job)
        #sys.exit(33)

        try:
            quality_total += int(job['quality'])
            startup_max += int(job['salary_max'])
            equity_max += float(job['equity_min'])
            equity_vest += float(job['equity_vest'])
            equity_cliff += float(job['equity_cliff'])
            count += 1
            output.append(job)
        except:
           # print "This are jobs that didn't have 100% data quality thus were not counted"
            #print json.dumps(job)
            pass
    #sys.exit(44)
    # avgs
    quality_total /= count
    startup_max /= count
    equity_max  /= count
    equity_cliff /= count


    '''  print '%f quality_total' % quality_total
    print '%f startup_max' % startup_max
    print '%f equity_max' % equity_max
    print '%f equity_cliff' % equity_cliff
    print '%f equity_vest' % equity_vest
    print '%f count' % count'''
    return {'output':output}, {'stats':{'quality_total':quality_total, 'startup_max':startup_max, 'equity_max':equity_max, 'equity_cliff':equity_cliff}}




#pprint(job_search_by_location(al,1692,"full-time"))#
#print json.dumps(stats(job_search_by_location(al,1692,"full-time")))

# jobs,quality_total,startup_max,equity_max,equity_cliff

def algo(jobs,*args):

    # unpack stats
    for arg in args:
        quality_total = arg['stats']['quality_total']
        startup_max = arg['stats']['startup_max']
        equity_max = arg['stats']['equity_max']
        equity_cliff = arg['stats']['equity_cliff']

    #print startup_max
    #sys.exit(444)

    for job in jobs['output']:
        print job.values()
        sys.exit(33)
    #for j in jobs:
        #print
        #print a['stats']['startup_max']
        #sys.exit(44)
    for job in jobs:
        print job
    sys.exit(33)

input_algo = stats(job_search_by_location(al,1692,"full-time"))

print algo(*input_algo)

sys.exit(33)




print pagination(al.get_tag_jobs,1692)

sys.exit(33)
#pprint(job_search_by_location(al,1629,"full-time"))

##page = al.get_tag_jobs(1692,page=3)
#print page['last_page']
#print page['page']

#pprint(me(al))




def getSkills(angel,level=3):
    '''
    Return a dic of skills based on the skills tag for users
    :param angel:
    :return:
    '''
    skills = []
    for x in angel.get_self()['skills']:
        #print x['id']
        if x['level'] >= level:
            #print x['name']
            skills.append(x['id'])
  #  print skills
    return skills


# search for jobs based on the skills i'm best at

def jobs_by_id(angel,skills_ids):
    for skill in skills_ids:
        print skill
        companies = []
        for employer in angel.get_tag_jobs(skill)['jobs']:
            if employer['startup']['quality'] > 8:
                companies
           # print employer['name']['quality']
            sys.exit(187)

        '''    for startup in json.dumps(employer['startup']):
                print startup['name']
                print type(startup)
                sys.exit(888)

            sys.exit(187)
             if startup['quality'] > 7:
                    print employer['quality']
                    companies.append()'''




#pprint(getSkills(al,3))
#pprint(al.get_tag_jobs(98210))
#jobs_by_id(al,getSkills(al,3))



#angel.get_tag_jobs(id)
#print al.get_jobs(page=1)



#print al.get_search('bitcoin','Startup')
#print al.get_startup('page=1')
#print json.dumps(al.get_self()['skills'])

#print al.get_tags('1')
#print first_page_jobs