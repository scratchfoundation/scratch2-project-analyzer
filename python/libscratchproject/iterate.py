"""
A script to iterate over all Scratch 2.0 projects.
"""
import project

start_id = 10000000 # start of scratch 2.0 projects, 10 million
end_id = 11784029 # update this by querying scratch sql: select id from projects_project order by id desc limit 1;
total_projects = 0
make_a_block_ids = set()

for project_id in range(start_id,end_id):
    proj = None
    try:
        proj = project.Project(project_id)
        total_projects += 1
    
    except Exception as e:
        # ignore folder not existing and unparsable json
        pass

    if proj:

        # process data here

        if proj.uses_make_a_block():
            make_a_block_ids.add(project_id)

with open('make_a_block_ids', 'wb') as f:
    for project_id in make_a_block_ids:
        f.write(project_id)
print len(make_a_block_ids), 'out of', len(total_projects)
