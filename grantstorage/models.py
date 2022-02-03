# Grant
class UserGrantInfoResponse(object):
    def __init__(self, grant, group):
        self.grant = grant
        self.group = group

# class Resources(models.Model):
#     cpu_hours = models.IntegerField()
#     max_walltime = models.IntegerField()
#
#
# class TeamMembers(models.Model):
#     plg_login = models.TextField()
#
#
# class Allocations(models.Model):
#     grant_name = models.TextField()
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     provider = models.TextField()
#     resource = models.TextField()
#     resources = models.ForeignKey(Resources, on_delete=models.RESTRICT)
#     site = models.TextField()
#
#
# class Grant(models.Model):
#     name = models.TextField()
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     state = models.TextField()
#     allocations = models.ForeignKey(Allocations, on_delete=models.RESTRICT)
#     team = models.TextField()
#     team_members = models.ForeignKey(TeamMembers, on_delete=models.RESTRICT)
#
#
# # ------
# class Grant2(object):
#     def __init__(self, name, start, end, state, allocations, team, team_members):
#         self.name = name
#         self.start = start
#         self.end = end
#         self.state = state
#         self.allocations = allocations
#         self.team = team
#         self.team_members = team_members
# # User
# class AffiliationList(models.Model):
#     end = models.TextField()
#     status = models.TextField()
#     type = models.TextField()
#     units = models.TextField()
#
#
# class User(models.Model):
#     # affiliation_list = models.ForeignKey(AffiliationList, on_delete=models.CASCADE, default=1)
#     email = models.TextField()
#     first_name = models.TextField()
#     i_d = models.IntegerField()
#     last_name = models.TextField()
#     login = models.TextField()
#     opi = models.TextField()
#     service_list = models.TextField()
#     status = models.TextField()
#
#
# # Group
# class Group(models.Model):
#     description = models.TextField()
#     name = models.TextField()
#     status = models.TextField()
#     teamId = models.TextField()
#     teamLeaders = models.TextField()
#     teamMembers = models.TextField()
#     type = models.TextField()
