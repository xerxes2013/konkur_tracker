import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'models.dart';
import 'history_screen.dart';

class ReportEntryScreen extends StatefulWidget {
  const ReportEntryScreen({super.key});

  @override
  State<ReportEntryScreen> createState() => _ReportEntryScreenState();
}

class _ReportEntryScreenState extends State<ReportEntryScreen> {
  final DailyReport report = DailyReport(date: DateTime.now(), slots: [StudySlot()]);

  final List<String> subjects = [
    'زیست‌شناسی', 'شیمی', 'فیزیک', 'ریاضیات', 'زمین‌شناسی',
    'ادبیات فارسی', 'دین و زندگی', 'عربی', 'زبان انگلیسی', 'سایر'
  ];

  Future<void> _pickTime(BuildContext context, bool isStart, StudySlot slot) async {
    final picked = await showTimePicker(
      context: context,
      initialTime: const TimeOfDay(hour: 8, minute: 0),
      builder: (context, child) {
        return Theme(
          data: ThemeData.dark().copyWith(
            colorScheme: const ColorScheme.dark(
              primary: Color(0xFF38BDF8),
              surface: Color(0xFF1E293B),
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() {
        final formatted = '${picked.hour.toString().padLeft(2, '0')}:${picked.minute.toString().padLeft(2, '0')}';
        if (isStart) {
          slot.startTime = formatted;
        } else {
          slot.endTime = formatted;
        }
      });
    }
  }

  Future<void> _saveReportLocally() async {
    final prefs = await SharedPreferences.getInstance();
    List<String> history = prefs.getStringList('saved_reports') ?? [];
    history.add(report.toJson());
    await prefs.setStringList('saved_reports', history);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('✨ گزارش روزانه با موفقیت ذخیره شد!'),
          backgroundColor: Color(0xFF10B981),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: const Text('ثبت گزارش روزانه', style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white)),
          actions: [
            IconButton(
              icon: const Icon(Icons.analytics_outlined, color: Color(0xFF38BDF8), size: 28),
              tooltip: 'آرشیو و نمودارها',
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen()));
              },
            ),
          ],
        ),
        body: ListView(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          children: [
            _buildSatisfactionCard(),
            const SizedBox(height: 16),
            ...report.slots.asMap().entries.map((entry) => _buildSlotCard(entry.key, entry.value)),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () => setState(() => report.slots.add(StudySlot())),
              icon: const Icon(Icons.add_circle_outline, color: Color(0xFF38BDF8)),
              label: const Text('افزودن پارت جدید', style: TextStyle(color: Color(0xFF38BDF8), fontWeight: FontWeight.bold)),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Color(0xFF38BDF8), width: 1.5),
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _saveReportLocally,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF38BDF8),
                foregroundColor: const Color(0xFF0F172A),
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              ),
              child: const Text('ذخیره و ثبت گزارش', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildSatisfactionCard() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white12),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('میزان رضایت از مطالعه:', style: TextStyle(color: Colors.white70, fontSize: 14)),
              Text('${report.satisfactionScore.toInt()} از ۱۰ ⭐', style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 18)),
            ],
          ),
          Slider(
            value: report.satisfactionScore,
            min: 1,
            max: 10,
            divisions: 9,
            activeColor: Colors.amber,
            inactiveColor: Colors.white12,
            onChanged: (v) => setState(() => report.satisfactionScore = v),
          ),
        ],
      ),
    );
  }

  Widget _buildSlotCard(int index, StudySlot slot) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('📌 پارت مطالعاتی ${index + 1}', style: const TextStyle(color: Color(0xFF38BDF8), fontWeight: FontWeight.bold, fontSize: 16)),
              if (report.slots.length > 1)
                IconButton(
                  icon: const Icon(Icons.delete_sweep, color: Colors.redAccent),
                  onPressed: () => setState(() => report.slots.removeAt(index)),
                ),
            ],
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            dropdownColor: const Color(0xFF1E293B),
            style: const TextStyle(color: Colors.white),
            value: slot.subject,
            decoration: _inputDecoration('انتخاب درس'),
            items: subjects.map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
            onChanged: (val) => setState(() => slot.subject = val ?? 'سایر'),
          ),
          if (slot.subject == 'سایر') ...[
            const SizedBox(height: 10),
            TextFormField(
              style: const TextStyle(color: Colors.white),
              decoration: _inputDecoration('نام درس را بنویسید'),
              onChanged: (v) => slot.customSubject = v,
            ),
          ],
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _buildTimeButton('شروع: ${slot.startTime}', () => _pickTime(context, true, slot)),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _buildTimeButton('پایان: ${slot.endTime}', () => _pickTime(context, false, slot)),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  style: const TextStyle(color: Colors.white),
                  decoration: _inputDecoration('منبع درسنامه'),
                  onChanged: (v) => slot.sourceStudy = v,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: TextFormField(
                  style: const TextStyle(color: Colors.white),
                  decoration: _inputDecoration('منبع تست'),
                  onChanged: (v) => slot.sourceTest = v,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              const Text('نوع تست: ', style: TextStyle(color: Colors.white70)),
              const SizedBox(width: 8),
              ChoiceChip(
                label: const Text('آموزشی'),
                selected: slot.testType == TestType.learning,
                selectedColor: const Color(0xFF38BDF8),
                onSelected: (_) => setState(() => slot.testType = TestType.learning),
              ),
              const SizedBox(width: 8),
              ChoiceChip(
                label: const Text('زمان‌دار'),
                selected: slot.testType == TestType.timed,
                selectedColor: const Color(0xFF38BDF8),
                onSelected: (_) => setState(() => slot.testType = TestType.timed),
              ),
            ],
          ),
          if (slot.testType == TestType.timed) ...[
            const SizedBox(height: 10),
            TextFormField(
              keyboardType: TextInputType.number,
              style: const TextStyle(color: Colors.white),
              decoration: _inputDecoration('مدت زمان آزمون (دقیقه)'),
              onChanged: (v) => slot.timedDurationMin = int.tryParse(v),
            ),
          ],
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _buildNumberBox('صحیح', Colors.greenAccent, (v) => slot.correctAnswers = int.tryParse(v) ?? 0)),
              const SizedBox(width: 6),
              Expanded(child: _buildNumberBox('غلط', Colors.redAccent, (v) => slot.wrongAnswers = int.tryParse(v) ?? 0)),
              const SizedBox(width: 6),
              Expanded(child: _buildNumberBox('نزده', Colors.grey, (v) => slot.unattemptedAnswers = int.tryParse(v) ?? 0)),
              const SizedBox(width: 6),
              Expanded(child: _buildNumberBox('شک‌دار', Colors.amberAccent, (v) => slot.doubtfulAnswers = int.tryParse(v) ?? 0)),
            ],
          ),
          const SizedBox(height: 10),
          TextFormField(
            style: const TextStyle(color: Colors.white),
            decoration: _inputDecoration('نکات و یادداشت'),
            onChanged: (v) => slot.notes = v,
          ),
        ],
      ),
    );
  }

  Widget _buildTimeButton(String label, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12),
        decoration: BoxDecoration(
          color: const Color(0xFF334155),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.access_time, size: 18, color: Color(0xFF38BDF8)),
              const SizedBox(width: 6),
              Text(label, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNumberBox(String label, Color color, Function(String) onChanged) {
    return TextFormField(
      textAlign: TextAlign.center,
      keyboardType: TextInputType.number,
      style: TextStyle(color: color, fontWeight: FontWeight.bold),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: TextStyle(color: color, fontSize: 12),
        filled: true,
        fillColor: const Color(0xFF334155),
        contentPadding: const EdgeInsets.symmetric(vertical: 10),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
      ),
      onChanged: onChanged,
    );
  }

  InputDecoration _inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.white54, fontSize: 13),
      filled: true,
      fillColor: const Color(0xFF334155),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
    );
  }
}