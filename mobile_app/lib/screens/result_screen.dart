import 'package:flutter/material.dart';
import '../models/ats_result.dart';

class ResultScreen extends StatelessWidget {
  final ATSResult atsResult;
  final Map<String, dynamic> parsedResume;

  const ResultScreen({
    super.key,
    required this.atsResult,
    required this.parsedResume,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analysis Results'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Score Card
              Card(
                color: _getScoreColor(atsResult.totalScore),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      Text(
                        'ATS Score',
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        '${atsResult.totalScore}/100',
                        style: const TextStyle(
                          fontSize: 48,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        atsResult.grade,
                        style: const TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 16),
                      LinearProgressIndicator(
                        value: atsResult.totalScore / 100,
                        backgroundColor: Colors.white.withOpacity(0.3),
                        valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                        minHeight: 8,
                      ),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 24),
              
              // Detailed Feedback
              Text(
                'Detailed Analysis',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              
              ...atsResult.detailedFeedback.entries.map((entry) {
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ExpansionTile(
                    title: Text(entry.key),
                    subtitle: Text(
                      '${entry.value['score']}/${entry.value['max']} points',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: (entry.value['feedback'] as List)
                              .map((feedback) => Padding(
                                padding: const EdgeInsets.only(bottom: 8.0),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Icon(
                                      _getFeedbackIcon(feedback),
                                      size: 16,
                                      color: _getFeedbackColor(feedback),
                                    ),
                                    const SizedBox(width: 8),
                                    Expanded(
                                      child: Text(
                                        feedback.toString(),
                                        style: const TextStyle(fontSize: 14),
                                      ),
                                    ),
                                  ],
                                ),
                              ))
                              .toList(),
                        ),
                      ),
                    ],
                  ),
                );
              }),
              
              const SizedBox(height: 24),
              
              // Key Insights
              Text(
                'Key Insights',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildInsightRow('Email', parsedResume['email'] ?? 'Not found'),
                      _buildInsightRow('Phone', parsedResume['phone']?.join(', ') ?? 'Not found'),
                      _buildInsightRow('Word Count', parsedResume['word_count']?.toString() ?? '0'),
                      _buildInsightRow('Action Verbs', parsedResume['action_verb_count']?.toString() ?? '0'),
                      _buildInsightRow(
                        'Quantifiable Results',
                        parsedResume['has_quantifiable_results'] == true ? 'Yes' : 'No',
                      ),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 24),
              
              // Recommendations
              if (_getRecommendations(parsedResume, atsResult.totalScore).isNotEmpty) ...[
                Text(
                  'Recommendations',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 16),
                
                ..._getRecommendations(parsedResume, atsResult.totalScore).map((rec) {
                  return Card(
                    color: Colors.orange.shade900.withOpacity(0.3),
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        children: [
                          const Icon(Icons.warning_amber, color: Colors.orange),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(rec),
                          ),
                        ],
                      ),
                    ),
                  );
                }),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInsightRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(color: Colors.grey),
          ),
          Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }

  Color _getScoreColor(int score) {
    if (score >= 80) return Colors.green;
    if (score >= 60) return Colors.orange;
    return Colors.red;
  }

  IconData _getFeedbackIcon(String feedback) {
    if (feedback.contains('✓')) return Icons.check_circle;
    if (feedback.contains('⚠')) return Icons.warning;
    return Icons.cancel;
  }

  Color _getFeedbackColor(String feedback) {
    if (feedback.contains('✓')) return Colors.green;
    if (feedback.contains('⚠')) return Colors.orange;
    return Colors.red;
  }

  List<String> _getRecommendations(Map<String, dynamic> parsed, int score) {
    List<String> recommendations = [];
    
    if (score < 70) {
      recommendations.add('Critical: Your resume needs significant improvements to pass ATS screening.');
    }
    if (parsed['email'] == null || parsed['email'].toString().isEmpty) {
      recommendations.add('Add a professional email address');
    }
    if (parsed['has_quantifiable_results'] != true) {
      recommendations.add('Add quantifiable achievements (e.g., "Increased sales by 25%")');
    }
    if ((parsed['action_verb_count'] ?? 0) < 5) {
      recommendations.add('Use more action verbs (achieved, improved, developed, etc.)');
    }
    
    return recommendations;
  }
}
