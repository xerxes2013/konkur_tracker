import 'package:flutter/material.dart';
import 'models.dart';

class ReportEntryScreen extends StatefulWidget {
  const ReportEntryScreen({super.key});

  @override
  State<ReportEntryScreen> createState() => _ReportEntryScreenState();
}

class _ReportEntryScreenState extends State<ReportEntryScreen> {
  final DailyReport report = DailyReport(date: DateTime.now(), slots: [StudySlot()]);

  final List<String> subjects = [
    'زیست‌شناسی', 'شیمی', 'فیزیک', 'ریاضیات', 'زمین‌شناسی', 'سایر'
  ];

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        backgroundColor: const Color(0xFFF4F6F9),
        appBar: AppBar(
          title: const Text('ثبت گزارش کار شبانه', style: TextStyle(fontWeight: FontWeight.bold)),
          centerTitle: true,
          backgroundColor: const Color(0xFF0F172A),
          foregroundColor: Colors.white,
        ),
        body: ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            _buildSatisfactionCard(),
            const SizedBox(height: 16),
            const Text(
              'پارت‌های مطالعاتی',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
            const SizedBox(height: 8),
            // ساخت لیست کارت‌های پارت‌ها
            ...report.slots.asMap().entries.map((entry) {
              return _buildSlotCard(entry.key, entry.value);
            }),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: () {
                setState(() {
                  report.slots.add(StudySlot());
                });
              },
              icon: const Icon(Icons.add),
              label: const Text('افزودن پارت درسی جدید'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0284C7),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: () {
                // ارسال به مرحله بعد (محاسبه و دریافت اسکرین‌تایم)
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('گزارش ذخیره شد! آماده اتصال به مرحله اسکرین‌تایم')),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF10B981),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text('تایید و رفتن به بخش آمار گوشی', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }

  // ۱. کارت امتیاز رضایت از روز
  Widget _buildSatisfactionCard() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('میزان رضایت از مطالعه امروز:', style: TextStyle(fontWeight: FontWeight.bold)),
                Text(
                  '${report.satisfactionScore.toInt()} از 10 ⭐',
                  style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.amber, fontSize: 16),
                ),
              ],
            ),
            Slider(
              value: report.satisfactionScore,
              min: 1,
              max: 10,
              divisions: 9,
              activeColor: Colors.amber[700],
              onChanged: (val) {
                setState(() => report.satisfactionScore = val);
              },
            ),
          ],
        ),
      ),
    );
  }

  // ۲. کارت پارت مطالعه اختصاصی
  Widget _buildSlotCard(int index, StudySlot slot) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('پارت شماره ${index + 1}', style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF0F172A))),
                if (report.slots.length > 1)
                  IconButton(
                    icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                    onPressed: () => setState(() => report.slots.removeAt(index)),
                  )
              ],
            ),
            const Divider(),
            DropdownButtonFormField<String>(
              value: slot.subject.isEmpty ? null : slot.subject,
              decoration: const InputDecoration(labelText: 'نام درس'),
              items: subjects.map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
              onChanged: (val) => setState(() => slot.subject = val ?? ''),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    decoration: const InputDecoration(labelText: 'ساعت شروع (مثلا 08:00)', hintText: '08:00'),
                    onChanged: (val) => slot.startTime = val,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: TextFormField(
                    decoration: const InputDecoration(labelText: 'ساعت پایان (مثلا 10:15)', hintText: '10:15'),
                    onChanged: (val) => slot.endTime = val,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    decoration: const InputDecoration(labelText: 'منبع درسنامه'),
                    onChanged: (val) => slot.sourceStudy = val,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: TextFormField(
                    decoration: const InputDecoration(labelText: 'منبع تست'),
                    onChanged: (val) => slot.sourceTest = val,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            // نوع تست‌زنی (آموزشی / زمان‌دار)
            Row(
              children: [
                const Text('نوع تست: '),
                ChoiceChip(
                  label: const Text('آموزشی'),
                  selected: slot.testType == TestType.learning,
                  onSelected: (val) => setState(() => slot.testType = TestType.learning),
                ),
                const SizedBox(width: 8),
                ChoiceChip(
                  label: const Text('زمان‌دار'),
                  selected: slot.testType == TestType.timed,
                  onSelected: (val) => setState(() => slot.testType = TestType.timed),
                ),
              ],
            ),
            if (slot.testType == TestType.timed) ...[
              const SizedBox(height: 10),
              TextFormField(
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'مدت زمان آزمون (دقیقه)'),
                onChanged: (val) => slot.timedDurationMin = int.tryParse(val),
              ),
            ],
            const SizedBox(height: 14),
            // فیلدهای تست: صحیح، غلط، نزده، شک‌دار
            Row(
              children: [
                Expanded(child: _buildNumberField('صحیح', (v) => slot.correctAnswers = int.tryParse(v) ?? 0, Colors.green)),
                const SizedBox(width: 6),
                Expanded(child: _buildNumberField('غلط', (v) => slot.wrongAnswers = int.tryParse(v) ?? 0, Colors.red)),
                const SizedBox(width: 6),
                Expanded(child: _buildNumberField('نزده', (v) => slot.unattemptedAnswers = int.tryParse(v) ?? 0, Colors.grey)),
                const SizedBox(width: 6),
                Expanded(child: _buildNumberField('شک‌دار', (v) => slot.doubtfulAnswers = int.tryParse(v) ?? 0, Colors.amber)),
              ],
            ),
            const SizedBox(height: 10),
            TextFormField(
              maxLines: 2,
              decoration: const InputDecoration(labelText: 'توضیحات و نکات این پارت'),
              onChanged: (val) => slot.notes = val,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNumberField(String label, Function(String) onChanged, Color color) {
    return TextFormField(
      keyboardType: TextInputType.number,
      textAlign: TextAlign.center,
      decoration: InputDecoration(
        labelText: label,
        labelStyle: TextStyle(color: color, fontSize: 13),
        contentPadding: const EdgeInsets.symmetric(vertical: 8),
      ),
      onChanged: onChanged,
    );
  }
}