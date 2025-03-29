# #all code has been commented out to not interfere with the DB for the moment, will be connected properly later
# # right now it exists, just for algorithm review when designing DB structure.
# class User:
#     def __init__(self, major, classes_can_tutor, classes_needed, initial_rating=5.0):
#         self.major = major
#         self.classes_can_tutor = classes_can_tutor
#         self.classes_needed = classes_needed
#         self.show_as_backup = True
#         self.rating = initial_rating
#         self.total_ratings = 0
#         self.rating_history = []  # Store last 50 ratings
#         self.recent_interactions = []  # Store last 10 interaction timestamps
#
#     def update_rating(self, new_rating, timestamp):
#         # Keep only last 50 ratings for rolling average
#         if len(self.rating_history) >= 50:
#             self.rating_history.pop(0)
#         self.rating_history.append(new_rating)
#
#         # Store interaction timestamp
#         if len(self.recent_interactions) >= 10:
#             self.recent_interactions.pop(0)
#         self.recent_interactions.append(timestamp)
#
#         # Weight recent ratings more heavily with exponential decay
#         weighted_sum = 0
#         total_weight = 0
#         for i, rating in enumerate(self.rating_history):
#             weight = 2 ** i  # Exponential weighting
#             weighted_sum += rating * weight
#             total_weight += weight
#
#         self.rating = weighted_sum / total_weight
#         self.total_ratings += 1
#
#     def get_activity_score(self, current_time):
#         # Calculate activity score based on recent interactions
#         if not self.recent_interactions:
#             return 0.5
#
#         last_interaction = max(self.recent_interactions)
#         days_since_last = (current_time - last_interaction).days
#         return max(0.5, 1 - (days_since_last / 30))  # Decay over 30 days
#
#     def get_penalty_multiplier(self):
#         if self.total_ratings < 5:
#             return 0.7  # New user penalty
#         elif self.rating < 4.0:
#             return 0.8
#         elif self.rating < 3.0:
#             return 0.4
#         elif self.rating < 2.0:
#             return 0.1
#         return 1.0
#
#
# def find_matches(current_user, all_users, target_class, current_time):
#     # First filter: Find users who need classes current user can tutor
#     primary_matches = [
#         user for user in all_users
#         if target_class in user.classes_needed
#            and any(cls in current_user.classes_can_tutor for cls in user.classes_needed)
#     ]
#
#     # Calculate match scores
#     def get_match_score(user):
#         rating_score = user.rating * user.get_penalty_multiplier()
#         activity_score = user.get_activity_score(current_time)
#         major_bonus = 1.2 if user.major == current_user.major else 1.0
#         return rating_score * activity_score * major_bonus
#
#     # Sort all matches by composite score
#     primary_matches.sort(key=get_match_score, reverse=True)
#
#     if not primary_matches:
#         backup_matches = [
#             user for user in all_users
#             if target_class in user.classes_can_tutor
#                and user.show_as_backup
#                and user.rating >= 3.0
#                and user.get_activity_score(current_time) >= 0.7  # Active users only
#         ]
#         backup_matches.sort(key=get_match_score, reverse=True)
#         return backup_matches
#
#     return primary_matches