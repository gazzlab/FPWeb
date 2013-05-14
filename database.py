from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from itertools import groupby
import logging
log = logging.getLogger('db')


db = SQLAlchemy()


MYSQL_CONN = 'mysql+mysqldb://%(db_user)s:%(db_pw)s@%(db_host)s/%(db_name)s'


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

  date = db.Column(db.DateTime())
  response = db.Column(db.Integer())
  sessionCount = db.Column(db.Integer())
  trialCount = db.Column(db.Integer())
  duration = db.Column(db.Integer())

  def __init__(self,
    date=-1.0,
    response=-1.0,
    sessionCount=-1.0,
    trialCount=-1.0,
    duration=-1.0,
    ):
    log.debug('Creating MediTrain record, date: %r', date)
    self.date = date
    self.response = response
    self.sessionCount = sessionCount
    self.trialCount = trialCount
    self.duration = duration


# Trial,Session Id,Category Id,Block Id,Trial,Exemplars,Morph Level,Morph Stimulus,RT,Response,Accuracy

class RecordsTrainCat(db.Model):

  study_ID = 'traincat'

  __tablename__ = 'rec1'

  id = db.Column(db.Integer, primary_key=True)

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

  id = db.Column(db.Integer, primary_key=True)

  #MediTrainPre_answerNames={
  #'How noisy is your environment right now?':environmentalNoise',
  #'How awake/alert are you right now, on a scale of 1-4?':'alertness',
  #'Have you consumed any caffeine in the last hour?':'caffeineHour'}


  environmentalNoise = db.Column(db.String(50))
  alertness = db.Column(db.String(50))
  caffeineHour = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    environmentalNoise=-1.0,
    alertness=-1.0,
    caffeineHour=-1.0,
    timeStamp=-1.0,
    ):
    self.environmentalNoise = environmentalNoise
    self.alertness = alertness
    self.caffeineHour = caffieneHour
    self.timeStamp = timeStamp


class RecordsMediTrainPost(db.Model):

  study_ID = 'MediTrainPost'

  __tablename__ = 'rec4'

  id = db.Column(db.Integer, primary_key=True)

  postTrainingLevel = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    postTrainingLevel=-1.0,
    timeStamp=-1.0,
    ):
    self.postTrainingLevel = postTrainingLevel
    self.timeStamp = timeStamp



class RecordsMediTrainSleep(db.Model):

  study_ID = 'MediTrainSleep'

  __tablename__ = 'rec5'

  id = db.Column(db.Integer, primary_key=True)

  #MediTrainSleep_answerNames={
  #'What time did you go to bed last night?':'bedTime',
  #'About how long did it take you to fall asleep last night?':'SOL',
  #'How many times did you wake up last night?':'nightWakes',
  #'What time did you get out of bed this morning?':'wakeTime',
  #'Approximately how many hours were you asleep last night?':'hoursAsleep',
  #'How well do you feel you slept last night, on a scale of 1-7?':'sleepQuality'
  #}

  bedTime = db.Column(db.String(50))
  SOL=db.Column(db.String(50))
  nightWakes=db.Column(db.String(50))
  wakeTime=db.Column(db.String(50))
  hoursAsleep=db.Column(db.String(50))
  sleepQuality=db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    bedTime=-1.0,
    SOL=-1.0,
    nightWakes=-1.0,
    wakeTime=-1.0,
    hoursAsleep=-1.0,
    sleepQuality=-1.0,
    timeStamp=-1.0,
    ):
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

  #'Which saliva sample are you taking?'=salivaSample

  salivaSample = db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    salivaSample=-1.0,
    timeStamp=-1.0,
    ):
    self.salivaSample = salivaSample
    self.timeStamp = timeStamp



class RecordsDATPre(db.Model):

  study_ID = 'DATPre'

  __tablename__ = 'rec7'

  id = db.Column(db.Integer, primary_key=True)

  #'Did anything good or bad happen today yet?'=whatHappened
  #'How are you feeling today, on a scale from 0-5?'=feelingToday
  #'What time did you wake up this morning?'=morningWakeTime
  #'How many hours of sleep did you get last night?'=hoursSleep
  #'How long did it take you to fall asleep last night, from getting into bed to actually falling asleep?'=sleepOnsetHours
  #'On a scale from 1-10, how "hyper" or "energetic" are you feeling today so far?'=energetic
  #'Have you had coffee yet today?'=coffeeYet
  #'How many days a week do you drink coffee in a normal week?'=coffeeDaysPerWeek


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

  id = db.Column(db.Integer, primary_key=True)

  #'What level did you get to?'=levelDATPost
  #'How enjoyable was this training session, on a scale of 1-5?'=enjoyableTraining
  #'How distracted were you during this training session, on a scale of 1-5?'=distractedTraining
  #'In what position were you playing the game?'=gamePosition
  #'Was the iPad:'=iPadPosition

  levelDATPost = db.Column(db.String(50))
  enjoyableTraining=db.Column(db.String(50))
  distractedTraining=db.Column(db.String(50))
  gamePosition=db.Column(db.String(50))
  iPadPosition=db.Column(db.String(50))
  timeStamp = db.Column(db.Float())

  def __init__(self,
    levelDATPost=-1.0,
    enjoyableTraining=-1.0,
    distractedTraining=-1.0,
    gamePosition=-1.0,
    iPadPosition=-1.0,
    timeStamp=-1.0,
    ):
    self.levelDATPost = levelDATPost
    self.enjoyableTraining=enjoyableTraining
    self.distractedTraining=distractedTraining
    self.gamePosition=gamePosition
    self.iPadPosition=iPadPosition
    self.timeStamp = timeStamp



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

