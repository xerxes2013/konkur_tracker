import 'package:flutter/material.dart';
import 'report_entry_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'گزارش کار آکادمی ۲۰',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'Vazir', // یا فونت پیش‌فرض
        primarySwatch: Colors.blue,
      ),
      home: const ReportEntryScreen(),
    );
  }
}