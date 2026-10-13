import 'dart:convert';

enum TestType { learning, timed }

class StudySlot {
  String subject;
  String customSubject; // برای زمانی که سایر انتخاب شد
  String startTime;
  String endTime;
  String sourceStudy;
  String sourceTest;
  TestType testType;
  int? timedDurationMin;
  int correctAnswers;
  int wrongAnswers;
  int unattemptedAnswers;
  int doubtfulAnswers;
  String notes;

  StudySlot({
    this.subject = 'زیست‌شناسی',
    this.customSubject = '',
    this.startTime = '08:00',
    this.endTime = '09:30',
    this.sourceStudy = '',
    this.sourceTest = '',
    this.testType = TestType.learning,
    this.timedDurationMin,
    this.correctAnswers = 0,
    this.wrongAnswers = 0,
    this.unattemptedAnswers = 0,
    this.doubtfulAnswers = 0,
    this.notes = '',
  });

  String get displaySubject => subject == 'سایر' ? (customSubject.isEmpty ? 'نامشخص' : customSubject) : subject;

  int get totalTests => correctAnswers + wrongAnswers + unattemptedAnswers;

  double get scorePercentage {
    if (totalTests == 0) return 0.0;
    double score = ((correctAnswers * 3) - wrongAnswers) / (totalTests * 3) * 100;
    return score < 0 ? 0 : score;
  }

  Map<String, dynamic> toMap() => {
    'subject': displaySubject,
    'startTime': startTime,
    'endTime': endTime,
    'sourceStudy': sourceStudy,
    'sourceTest': sourceTest,
    'testType': testType.index,
    'timedDurationMin': timedDurationMin,
    'correctAnswers': correctAnswers,
    'wrongAnswers': wrongAnswers,
    'unattemptedAnswers': unattemptedAnswers,
    'doubtfulAnswers': doubtfulAnswers,
    'notes': notes,
  };

  factory StudySlot.fromMap(Map<String, dynamic> map) => StudySlot(
    subject: map['subject'] ?? '',
    startTime: map['startTime'] ?? '',
    endTime: map['endTime'] ?? '',
    sourceStudy: map['sourceStudy'] ?? '',
    sourceTest: map['sourceTest'] ?? '',
    testType: TestType.values[map['testType'] ?? 0],
    timedDurationMin: map['timedDurationMin'],
    correctAnswers: map['correctAnswers'] ?? 0,
    wrongAnswers: map['wrongAnswers'] ?? 0,
    unattemptedAnswers: map['unattemptedAnswers'] ?? 0,
    doubtfulAnswers: map['doubtfulAnswers'] ?? 0,
    notes: map['notes'] ?? '',
  );
}

class DailyReport {
  DateTime date;
  double satisfactionScore;
  List<StudySlot> slots;

  DailyReport({
    required this.date,
    this.satisfactionScore = 7.0,
    List<StudySlot>? slots,
  }) : slots = slots ?? [];

  int get totalTests => slots.fold(0, (sum, item) => sum + item.totalTests);
  int get totalCorrect => slots.fold(0, (sum, item) => sum + item.correctAnswers);
  int get totalWrong => slots.fold(0, (sum, item) => sum + item.wrongAnswers);

  String toJson() => jsonEncode({
    'date': date.toIso8601String(),
    'satisfactionScore': satisfactionScore,
    'slots': slots.map((s) => s.toMap()).toList(),
  });

  factory DailyReport.fromJson(String jsonStr) {
    final map = jsonDecode(jsonStr);
    return DailyReport(
      date: DateTime.parse(map['date']),
      satisfactionScore: (map['satisfactionScore'] as num).toDouble(),
      slots: (map['slots'] as List).map((s) => StudySlot.fromMap(s)).toList(),
    );
  }
}