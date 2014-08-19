from time import mktime
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from itertools import groupby
import logging
log = logging.getLogger('db')


db = SQLAlchemy()


MYSQL_CONN = 'mysql+mysqldb://%(db_user)s:%(db_pw)s@%(db_host)s/%(db_name)s'


def get_field_names(record_class):
  return record_class.__table__.columns._data.keys()
  # This is apparently not in the sqlalchemy api.


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
  name = db.Column(db.String(50))
  fullname = db.Column(db.String(50))
  email = db.Column(db.String(50))
  password = db.Column(db.String(12))
  role = db.Column(db.String(50))

  def __init__(self, name, fullname, email, password):
    log.debug('Creating user %s %s, %s', name, fullname, email)
    self.name = name
    self.fullname = fullname
    self.email = email
    self.password = password
    self.role = 'subject'

  def __repr__(self):
    return "<User(%r, %r, %r)>" % (self.name, self.fullname, self.email)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    assert self.id is not None
    return unicode(self.id)


class RecordAny(db.Model):
  __tablename__ = 'polymorph'
  id = db.Column(db.Integer, primary_key=True)
  studyID = db.Column(db.String(50))
  subjectID = db.Column(db.String(50))
  raw_data = db.Column(db.String(1000))

  _studyID_attrgetter = lambda ra: ra.studyID

  @classmethod
  def by_studyID(class_):
    s = class_.query.all()
    s.sort(key=class_._studyID_attrgetter)
    for stid_group in groupby(s, class_._studyID_attrgetter):
      yield stid_group


class RecordsDat(db.Model):

  study_ID = 'DAT'

  __tablename__ = 'rec2'

  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  angleOfXVPlus = db.Column(db.Float())
  cueProbeTime = db.Column(db.Float())
  currentReleaseReactionTimeGoal = db.Column(db.Float())
  distanceFromProbe = db.Column(db.Float())
  informationOfTheCue = db.Column(db.Float())
  locationOfTargetInDegrees = db.Column(db.Float())
  reactionTime = db.Column(db.Float())
  releaseReactionTime = db.Column(db.Float())
  shouldPressProbe = db.Column(db.Float())
  sucsess = db.Column(db.Float())
  targetOnScreenTime = db.Column(db.Float())
  timeBetweenCueAndTarget = db.Column(db.Float())
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID =-1.0,
    angleOfXVPlus=-1.0,
    cueProbeTime=-1.0,
    currentReleaseReactionTimeGoal=-1.0,
    distanceFromProbe=-1.0,
    informationOfTheCue=-1.0,
    locationOfTargetInDegrees=-1.0,
    reactionTime=-1.0,
    releaseReactionTime=-1.0,
    shouldPressProbe=-1.0,
    sucsess=-1.0,
    targetOnScreenTime=-1.0,
    timeBetweenCueAndTarget=-1.0,
    timeStamp=-1.0,
    ):
    log.debug('Creating DAT record')
    self.subjectID = subjectID
    self.angleOfXVPlus = angleOfXVPlus
    self.cueProbeTime = cueProbeTime
    self.currentReleaseReactionTimeGoal = currentReleaseReactionTimeGoal
    self.distanceFromProbe = distanceFromProbe
    self.informationOfTheCue = informationOfTheCue
    self.locationOfTargetInDegrees = locationOfTargetInDegrees
    self.reactionTime = reactionTime
    self.releaseReactionTime = releaseReactionTime
    self.shouldPressProbe = shouldPressProbe
    self.sucsess = sucsess
    self.targetOnScreenTime = targetOnScreenTime
    self.timeBetweenCueAndTarget = timeBetweenCueAndTarget
    self.timeStamp = timeStamp


class RecordsMediTrain(db.Model):

  study_ID = 'meditrain'

  __tablename__ = 'rec0'

  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  date = db.Column(db.DateTime())
#  date_huh = db.Column(db.String(128))
  response = db.Column(db.Integer())
  sessionCount = db.Column(db.Integer())
  trialCount = db.Column(db.Integer())
  duration = db.Column(db.Integer())
#  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID =-1.0,
    date=-1.0,
    response=-1.0,
    sessionCount=-1.0,
    trialCount=-1.0,
    duration=-1.0,
    ):
    log.debug('Creating MediTrain record, date: %r', date)
    self.subjectID = subjectID
    try:
      self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
#      self.timeStamp = mktime(self.date.timetuple())
    except:
#      self.date_huh = date
      self.date = date
    self.response = response
    self.sessionCount = sessionCount
    self.trialCount = trialCount
    self.duration = duration

class RecordsMediTrainV2Session(db.Model):
    
    study_ID = 'testMeditrain'
    
    __tablename__ = 'meditrainTest'
    
    id = db.Column(db.Integer(), primary_key=True)

    sessionID = db.Column(db.String(55))
    subjectID = db.Column(db.String(50))
#    subject = db.relationship("RecordsMediTrainV2Subject", backref="sessions")
    miniSessions = db.relationship(RecordsMediTrainV2MiniSession.__tablename__, backref="session")
    survey = db.relationship(RecordsMediTrainV2Survey.__tablename__, uselist=False, backref="session")
    miniSessionCount = db.Column(db.Integer())
    cumulativeID = db.Column(db.Integer())
    day = db.Column(db.Integer())
    duration = db.Column(db.Float())
    endTimestamp = db.Column(db.Integer())
    month = db.Column(db.Integer())
    startTimestamp = db.Column(db.Integer())
    year = db.Column(db.Integer())
    
    def __init__(self,
                 sessionID=None,
                 subjectID=None,
                 cumulativeID=-1.0,
                 day=-1.0,
                 endTimestamp=-1.0,
                 miniSessions=None,
                 miniSessionCount=-1.0,
                 survey=None,
                 month=-1.0,
                 startTimestamp=-1.0,
                 duration=-1.0,
                 year=-1.0):
        log.debug('Creating MediTrain V2 Session record, sessionID: %r', sessionID)
        self.sessionID = sessionID
        self.subjectID = subjectID
        self.cumulativeID = cumulativeID
        self.day = day
        self.duration = duration
        self.endTimestamp = endTimestamp
        self.month = month
        self.startTimestamp = startTimestamp
        self.year = year
        self.miniSessionCount = miniSessionCount
        for miniSession in miniSessions:
            self.miniSessions.append(RecordsMediTrainV2MiniSession(miniSession))
        self.survey = RecordsMediTrainV2Survey(survey)

#class RecordsMediTrainV2Subject(db.Model):
#    study_ID = 'testMeditrain'
#
#    __tablename__ = 'meditrainTestSubject'
#
#    id = db.Column(db.Integer(), primary_key=True)
#
#    subjectID = db.Column(db.String(50))
#    daysCompleted = db.Column(db.Integer())
#    endTimestamp = db.Column(db.Integer())
#    lastSyncTime = db.Column(db.Integer())
#    meditationDuration = db.Column(db.Float())
#    startTimestamp = db.Column(db.Integer())
#
#    def __init__(self,
#                 subjectID =-1.0,
#                 daysCompleted = -1.0,
#	             endTimestamp = -1.0,
#                 lastSyncTime = -1.0,
#                 meditationDuration = -1.0,
#                 startTimestamp = -1.0):
#        log.debug('Creating MediTrain V2 Subject record, subjectID: %r', subjectID)
#        self.subjectID = subjectID
#        self.daysCompleted = daysCompleted
#        self.endTimestamp = endTimestamp
#        self.lastSyncTime = lastSyncTime
#        self.meditationDuration = meditationDuration
#        self.startTimestamp = startTimestamp

class RecordsMediTrainV2Survey(db.Model):
    study_ID = 'testMeditrain'

    __tablename__ = 'meditrainTestSurvey'

    id = db.Column(db.Integer(), primary_key=True)

    surveyID = db.Column(db.String(55))
    complete = db.Column(db.Boolean())
    cumulativeID = db.Column(db.Integer())
    question1 = db.Column(db.Boolean())
    question2 = db.Column(db.Integer())
    question3 = db.Column(db.Integer())
    timestamp = db.Column(db.Integer())
#    session_id = db.Column(db.Integer(), db.ForeignKey(RecordsMediTrainV2Session.__tablename__ + ".id"))
    subjectID = db.Column(db.String(50))
    sessionID = db.Column(db.String(55))

    def __init__(self,
                 surveyID = None,
                 complete = False,
                 cumulativeID = -1.0,
                 question1 = None,
                 question2 = -1.0,
                 question3 = -1.0,
                 timestamp = -1.0,
                 subjectID = None,
                 sessionID = None):
        log.debug('Creating MediTrain V2 Survey record, surveyID: %r', surveyID)
        self.surveyID = surveyID
        self.complete = complete
        self.cumulativeID = cumulativeID
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.timestamp = timestamp
        self.subjectID = subjectID
        self.sessionID = sessionID

class RecordsMediTrainV2MiniSession(db.Model):
    study_ID = 'testMeditrain'

    __tablename__ = 'meditrainTestMiniSession'

    id = db.Column(db.Integer(), primary_key=True)

    miniSessionID = db.Column(db.String(55))
    cumulativeID = db.Column(db.Integer())
    duration = db.Column(db.Float())
    endTime = db.Column(db.Integer())
    result = db.Column(db.Integer())
    startTime = db.Column(db.Integer())
#    session_id = db.Column(db.Integer(), db.ForeignKey(RecordsMediTrainV2Session.__tablename__ + ".id"))
    sessionID = db.Column(db.String(55))
    subjectID = db.Column(db.String(50))

    def __init__(self,
                 miniSessionID = None,
                 cumulativeID = -1.0,
                 duration = -1.0,
                 endTime = -1.0,
                 result = -1.0,
                 startTime = -1.0,
                 sessionID = None,
                 subjectID = None):
        log.debug('Creating MediTrain V2 MiniSession record, miniSessionID: %r', miniSessionID)
        self.miniSessionID = miniSessionID
        self.cumulativeID = cumulativeID
        self.duration = duration
        self.endTime = endTime
        self.result = result
        self.startTime = startTime
        self.sessionID = sessionID


# Trial,Session Id,Category Id,Block Id,Trial,Exemplars,Morph Level,Morph Stimulus,RT,Response,Accuracy

class RecordsTrainCat(db.Model):

  study_ID = 'traincat'

  __tablename__ = 'rec1'

  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  index = db.Column(db.Integer())
  sessionID = db.Column(db.Integer())
  categoryID = db.Column(db.Integer())
  blockID = db.Column(db.Integer())
  trial = db.Column(db.Integer())
  exemplars = db.Column(db.String(50)) # What is this and why are we saving it like this?
  morphLevel = db.Column(db.Integer())
  morphStimulus = db.Column(db.String(50))
  RT = db.Column(db.Float())
  response = db.Column(db.String(50))
  accuracy = db.Column(db.String(50))

  def __init__(self,
    subjectID =-1.0,
    index = -1.0,
    sessionID = -1.0,
    categoryID = -1.0,
    blockID = -1.0,
    trial = -1.0,
    exemplars = -1.0,
    morphLevel = -1.0,
    morphStimulus = -1.0,
    RT = -1.0,
    response =- 1.0,
    accuracy = -1.0,
    ):
    log.debug('Creating TrainCat record, sessionID: %r', sessionID)
    self.subjectID = subjectID
    self.index = index
    self.sessionID = sessionID
    self.categoryID = categoryID
    self.blockID = blockID
    self.trial = trial
    self.exemplars = exemplars
    self.morphLevel = morphLevel
    self.morphStimulus = morphStimulus
    self.RT = RT
    self.response = response
    self.accuracy = accuracy



class RecordsMediTrainPre(db.Model):

  study_ID = 'MediTrainPre'

  __tablename__ = 'rec3'

  field_map = {
    'Have you consumed any caffeine in the last hour?': 'caffeineHour',
    'How awake/alert are you right now, on a scale of 1-4?': 'alertness',
    'How noisy is your environment right now?': 'environmentalNoise',
    'What level did you reach in the training app, today?': 'alertness',  # IS THIS SUPPOSED TO BE ONE OF THESE?
    }

  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  environmentalNoise = db.Column(db.String(50))
  alertness = db.Column(db.String(50))
  caffeineHour = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID=-1.0,
    environmentalNoise=-1.0,
    alertness=-1.0,
    caffeineHour=-1.0,
    timeStamp=-1.0,
    ):
    self.subjectID = subjectID
    self.environmentalNoise = environmentalNoise
    self.alertness = alertness
    self.caffeineHour = caffeineHour
    self.timeStamp = timeStamp


class RecordsMediTrainPost(db.Model):

  study_ID = 'MediTrainPost'

  __tablename__ = 'rec4'

  field_map = {'How do you feel about your training session today?': 'postTrainingLevel'}

  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  postTrainingLevel = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID=-1.0,
    postTrainingLevel=-1.0,
    timeStamp=-1.0,
    ):
    self.subjectID = subjectID
    self.postTrainingLevel = postTrainingLevel
    self.timeStamp = timeStamp


class RecordsMediTrainSleep(db.Model):

  study_ID = 'MediTrainSleep'

  __tablename__ = 'rec5'

  field_map = {
    'About how long did it take you to fall asleep last night?': 'SOL',
    'Approximately how many hours were you asleep last night?': 'hoursAsleep',
    'How many times did you wake up last night?': 'nightWakes',
    'How well do you feel you slept last night, on a scale of 1-7?': 'sleepQuality',
    'What time did you get out of bed this morning?': 'wakeTime',
    'What time did you go to bed last night?': 'bedTime',
    }

  id = db.Column(db.Integer, primary_key=True)

  #MediTrainSleep_answerNames={
  #'What time did you go to bed last night?':'bedTime',
  #'About how long did it take you to fall asleep last night?':'SOL',
  #'How many times did you wake up last night?':'nightWakes',
  #'What time did you get out of bed this morning?':'wakeTime',
  #'Approximately how many hours were you asleep last night?':'hoursAsleep',
  #'How well do you feel you slept last night, on a scale of 1-7?':'sleepQuality'
  #}

  subjectID = db.Column(db.String(50))
  bedTime = db.Column(db.String(50))
  SOL=db.Column(db.String(50))
  nightWakes=db.Column(db.String(50))
  wakeTime=db.Column(db.String(50))
  hoursAsleep=db.Column(db.String(50))
  sleepQuality=db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID=-1.0,
    bedTime=-1.0,
    SOL=-1.0,
    nightWakes=-1.0,
    wakeTime=-1.0,
    hoursAsleep=-1.0,
    sleepQuality=-1.0,
    timeStamp=-1.0,
    ):
    self.subjectID = subjectID
    self.bedTime = bedTime
    self.SOL=SOL
    self.nightWakes=nightWakes
    self.wakeTime=wakeTime
    self.hoursAsleep=hoursAsleep
    self.sleepQuality=sleepQuality
    self.timeStamp = timeStamp

class RecordsMediTrainSaliva(db.Model):

  study_ID = 'MediTrainSaliva'

  __tablename__ = 'rec6'

  id = db.Column(db.Integer, primary_key=True)

  field_map = {'Which saliva sample are you taking?': 'salivaSample'}

  #'Which saliva sample are you taking?'=salivaSample

  subjectID = db.Column(db.String(50))
  salivaSample = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID,
    salivaSample,
    timeStamp,
    ):
    self.subjectID = subjectID
    self.salivaSample = salivaSample
    self.timeStamp = timeStamp



class RecordsDATPre(db.Model):

  study_ID = 'DATPre'

  __tablename__ = 'rec7'

  field_map = {
    'iPad #:':'iPadID',
    'Did anything good or bad happen today yet?': 'whatHappened',
    'Have you had coffee yet today?': 'coffeeYet',
    #'Have you consumed any caffeine in the last hour?': 'coffeeYet',  # IS THIS SUPPOSED TO BE ONE OF THESE?
    #'How awake/alert are you right now, on a scale of 1-4?': 'feelingToday',  # IS THIS SUPPOSED TO BE ONE OF THESE?
    'How are you feeling today, on a scale from 0-5': 'feelingToday',
    'How long did it take you to fall asleep last night, from getting into bed to actually falling asleep?': 'sleepOnsetHours',
    'How many days a week do you drink coffee in a normal week?': 'coffeeDaysPerWeek',
    'How many hours of sleep did you get last night?': 'hoursSleep',
    #'On a scale from 1-10, how "hyper" or "energetic" are you feeling today so far?': 'energetic',
    'On a scale from 1-10, how hyper or energetic are you feeling today so far?': 'energetic',
    'What time did you wake up this morning?': 'morningWakeTime',
    }

  id = db.Column(db.Integer, primary_key=True)

  #'Did anything good or bad happen today yet?'=whatHappened
  #'How are you feeling today, on a scale from 0-5?'=feelingToday
  #'What time did you wake up this morning?'=morningWakeTime
  #'How many hours of sleep did you get last night?'=hoursSleep
  #'How long did it take you to fall asleep last night, from getting into bed to actually falling asleep?'=sleepOnsetHours
  #'On a scale from 1-10, how "hyper" or "energetic" are you feeling today so far?'=energetic
  #'Have you had coffee yet today?'=coffeeYet
  #'How many days a week do you drink coffee in a normal week?'=coffeeDaysPerWeek

  subjectID = db.Column(db.String(50))
  iPadID = db.Column(db.String(50))
  whatHappened = db.Column(db.String(50))
  feelingToday=db.Column(db.String(50))
  morningWakeTime=db.Column(db.String(50))
  hoursSleep=db.Column(db.String(50))
  sleepOnsetHours=db.Column(db.String(50))
  energetic=db.Column(db.String(50))
  coffeeYet=db.Column(db.String(50))
  coffeeDaysPerWeek=db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID=-1.0,
    iPadID=-1.0,
    whatHappened=-1.0,
    feelingToday=-1.0,
    morningWakeTime=-1.0,
    hoursSleep=-1.0,
    sleepOnsetHours=-1.0,
    energetic=-1.0,
    coffeeYet=-1.0,
    coffeeDaysPerWeek=-1.0,
    timeStamp=-1.0,
    ):
    self.subjectID = subjectID
    self.iPadID=iPadID
    self.whatHappened = whatHappened
    self.feelingToday=feelingToday
    self.morningWakeTime=morningWakeTime
    self.hoursSleep=hoursSleep
    self.sleepOnsetHours=sleepOnsetHours
    self.energetic=energetic
    self.coffeeYet=coffeeYet
    self.coffeeDaysPerWeek=coffeeDaysPerWeek
    self.timeStamp = timeStamp


class RecordsDATPost(db.Model):

  study_ID = 'DATPost'

  __tablename__ = 'rec8'

  field_map = {
    'What level did you get to?':'levelDATPost',
    'How enjoyable was this training session, on a scale of 1-5?':'enjoyableTraining',
    'How distracted were you during this training session, on a scale of 1-5?':'distractedTraining',
    'In what position were you playing the game?':'gamePosition',
    'Was the iPad:':'iPadPosition',
    }
  
###commented questions below were from DATpre, not DATpost
  #  'Did anything good or bad happen today yet?': 'whatHappened',
  #  'How are you feeling today, on a scale from 0-5?': 'feelingToday',
  #  'How long did it take you to fall asleep last night, from getting into bed to actually falling asleep?': 'sleepOnsetHours',
  #  'How many hours of sleep did you get last night?': 'hoursSleep',
  #  'What time did you wake up this morning?': 'morningWakeTime',
    
  id = db.Column(db.Integer, primary_key=True)

  subjectID = db.Column(db.String(50))
  levelDATPost = db.Column(db.String(50))
  enjoyableTraining=db.Column(db.String(50))
  distractedTraining=db.Column(db.String(50))
  gamePosition=db.Column(db.String(50))
  iPadPosition=db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    subjectID=-1.0,
    levelDATPost=-1.0,
    enjoyableTraining=-1.0,
    distractedTraining=-1.0,
    gamePosition=-1.0,
    iPadPosition=-1.0,
    timeStamp=-1.0,
    ):
    self.subjectID = subjectID
    self.levelDATPost = levelDATPost
    self.enjoyableTraining=enjoyableTraining
    self.distractedTraining=distractedTraining
    self.gamePosition=gamePosition
    self.iPadPosition=iPadPosition
    self.timeStamp = timeStamp



class RecordsLeapDat(db.Model):

  study_ID = 'LeapDAT'

  __tablename__ = 'rec9'

  id = db.Column(db.Integer, primary_key=True)
  
  #two tables, one for 'players', one for 'test' data
  #fields in table 'players'
  # SET time_zone = "+00:00";
  subjectID = db.Column(db.String(50))
  date_of_birth = db.Column(db.DateTime)
  
  #fields in table 'test'
  trial_number = db.Column(db.String(50))
  time = db.Column(db.String(50))
  angle = db.Column(db.String(50))
  cue = db.Column(db.String(50))
  direction = db.Column(db.Integer(4))
  valid = db.Column(db.Integer(4))
  success = db.Column(db.Integer(4))
  no_response = db.Column(db.Integer(4))
  acceleration_time = db.Column(db.String(50))
  reaction_time = db.Column(db.String(50))
  hit_time = db.Column(db.String(50))
  timestamp=db.Column(db.Float())
  
  #fields in table 'test_coords'
  x = db.Column(db.String(4000))
  y = db.Column(db.String(4000))

  def __init__(self,  
    id =-1.0,
    player_id=-1.0,
    date_of_birth =-1.0,
    trial_number=-1.0,
    time=-1.0,
    angle=-1.0,
    cue=-1.0,
    direction=-1.0,
    valid=-1.0,
    success=-1.0,
    no_response=-1.0,
    acceleration_time=-1.0,
    reaction_time=-1.0,
    hit_time=-1.0,
    timestamp=-1.0,
    x=-1.0,
    y=-1.0,
    ):
    
    log.debug('Creating LeapDAT record')
    self.player_id = player_id
    self.date_of_birth = date_of_birth
    self.trial_number = trial_number
    self.time = time
    self.angle = angle
    self.cue = cue
    self.direction = direction
    self.valid = valid
    self.success = success
    self.no_response = no_response
    self.acceleration_time = acceleration_time
    self.reaction_time = reaction_time
    self.hit_time = hit_time
    self.timestamp=timestamp
    self.x=x
    self.y=y





class Profile(db.Model):

  __tablename__ = 'profile'

  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(50))
  lname = db.Column(db.String(50))
  sex = db.Column(db.Integer())
  birthdate = db.Column(db.DateTime())
  subject_id = db.Column(db.Integer())
  phone = db.Column(db.String(50))
  email = db.Column(db.String(50))
  language = db.Column(db.String(50))
  language_additional = db.Column(db.String(50))
  meditation = db.Column(db.String(50))
  meditation_description = db.Column(db.String(500))
  other_studies = db.Column(db.String(50))
  history = db.Column(db.String(50))
  history_explanation = db.Column(db.String(500))
  psychiatric = db.Column(db.Integer())
  psychiatric_describe = db.Column(db.String(500))
  learning_disabilities = db.Column(db.String(50))
  medications = db.Column(db.String(50))
  handedness = db.Column(db.Integer())
  school = db.Column(db.Integer())
  alcohol = db.Column(db.String(50))
  smoke = db.Column(db.Integer())
  exercise = db.Column(db.Integer())
  type_exercises = db.Column(db.String(100))
  hours_sleep = db.Column(db.String(50))

  def __init__(self,
    fname = -1.0,
    lname = -1.0,
    sex = -1.0,
    birthdate = -1.0,
    subject_id = -1.0,
    phone = -1.0,
    email = -1.0,
    language = -1.0,
    language_additional = -1.0,
    meditation = -1.0,
    meditation_description = -1.0,
    other_studies = -1.0,
    history = -1.0,
    history_explanation = -1.0,
    psychiatric = -1.0,
    psychiatric_describe = -1.0,
    learning_disabilities = -1.0,
    medications = -1.0,
    handedness = -1.0,
    school = -1.0,
    alcohol = -1.0,
    smoke = -1.0,
    exercise = -1.0,
    type_exercises = -1.0,
    hours_sleep = -1.0,
    ):
    self.fname = fname
    self.lname = lname
    self.sex = sex
    self.birthdate = birthdate
    self.subject_id = subject_id
    self.phone = phone
    self.email = email
    self.language = language
    self.language_additional = language_additional
    self.meditation = meditation
    self.meditation_description = meditation_description
    self.other_studies = other_studies
    self.history = history
    self.history_explanation = history_explanation
    self.psychiatric = psychiatric
    self.psychiatric_describe = psychiatric_describe
    self.learning_disabilities = learning_disabilities
    self.medications = medications
    self.handedness = handedness
    self.school = school
    self.alcohol = alcohol
    self.smoke = smoke
    self.exercise = exercise
    self.type_exercises = type_exercises
    self.hours_sleep = hours_sleep

