import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:share_plus/share_plus.dart';
import 'models.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<DailyReport> reports = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList('saved_reports') ?? [];
    setState(() {
      reports = list.map((item) => DailyReport.fromJson(item)).toList();
    });
  }

  void _shareSummary(String title, int totalTests, int correct, int wrong) {
    final text = '''
📊 $title | آکادمی دکتر اشکبوس (@Kh_Ashkboos)
━━━━━━━━━━━━━━━━━━
📝 مجموع کل تست‌ها: $totalTests
✅ تست‌های صحیح: $correct
❌ تست‌های غلط: $wrong
🎯 درصد خالص: ${totalTests > 0 ? (((correct * 3 - wrong) / (totalTests * 3)) * 100).toStringAsFixed(1) : 0}%
━━━━━━━━━━━━━━━━━━
ارسال شده از اپلیکیشن اختصاصی آکادمی ۲۰ 🚀
''';
    Share.share(text);
  }

  @override
  Widget build(BuildContext context) {
    final weekReports = reports.take(7).toList();
    final monthReports = reports.take(30).toList();

    int weekTests = weekReports.fold(0, (s, r) => s + r.totalTests);
    int weekCorrect = weekReports.fold(0, (s, r) => s + r.totalCorrect);
    int weekWrong = weekReports.fold(0, (s, r) => s + r.totalWrong);

    int monthTests = monthReports.fold(0, (s, r) => s + r.totalTests);
    int monthCorrect = monthReports.fold(0, (s, r) => s + r.totalCorrect);
    int monthWrong = monthReports.fold(0, (s, r) => s + r.totalWrong);

    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        appBar: AppBar(
          title: const Text('آرشیو هفتگی و ماهانه', style: TextStyle(fontWeight: FontWeight.bold)),
          backgroundColor: const Color(0xFF1E293B),
        ),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildStatCard('گزارش عملکرد ۷ روز اخیر (هفتگی)', weekTests, weekCorrect, weekWrong, () {
              _shareSummary('گزارش هفتگی', weekTests, weekCorrect, weekWrong);
            }),
            const SizedBox(height: 16),
            _buildStatCard('گزارش عملکرد ۳۰ روز اخیر (ماهانه)', monthTests, monthCorrect, monthWrong, () {
              _shareSummary('گزارش ماهانه', monthTests, monthCorrect, monthWrong);
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, int tests, int correct, int wrong, VoidCallback onShare) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
              IconButton(icon: const Icon(Icons.share, color: Color(0xFF38BDF8)), onPressed: onShare),
            ],
          ),
          const Divider(color: Colors.white12),
          Text('📝 کل تست‌ها: $tests', style: const TextStyle(color: Colors.white70)),
          const SizedBox(height: 4),
          Text('✅ صحیح: $correct | ❌ غلط: $wrong', style: const TextStyle(color: Colors.white70)),
        ],
      ),
    );
  }
}