enum TestType { learning, timed } // آموزشی یا زمان‌دار

class StudySlot {
  String subject;          // نام درس (زیست، فیزیک و...)
  String startTime;        // مثلاً 08:00
  String endTime;          // مثلا提 10:15
  String sourceStudy;      // منبع درسنامه
  String sourceTest;       // منبع تست
  TestType testType;       // آموزشی یا زمان‌دار
  int? timedDurationMin;   // مدت زمان تست اگر زمان‌دار باشد (به دقیقه)
  int correctAnswers;      // صحیح
  int wrongAnswers;        // غلط
  int unattemptedAnswers;  // نزده
  int doubtfulAnswers;     // شک‌دار
  String notes;            // توضیحات

  StudySlot({
    this.subject = '',
    this.startTime = '',
    this.endTime = '',
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

  // کل تست‌های این پارت
  int get totalTests => correctAnswers + wrongAnswers + unattemptedAnswers;

  // محاسبه درصد کنکوری پارت
  double get scorePercentage {
    if (totalTests == 0) return 0.0;
    double score = ((correctAnswers * 3) - wrongAnswers) / (totalTests * 3) * 100;
    return score < 0 ? 0 : score;
  }
}

class DailyReport {
  DateTime date;
  double satisfactionScore; // نمره رضایت بین ۱ تا ۱۰
  List<StudySlot> slots;

  DailyReport({
    required this.date,
    this.satisfactionScore = 5.0,
    List<StudySlot>? slots,
  }) : slots = slots ?? [];
}