class ATSResult {
  final int totalScore;
  final String grade;
  final Map<String, dynamic> detailedFeedback;

  ATSResult({
    required this.totalScore,
    required this.grade,
    required this.detailedFeedback,
  });

  factory ATSResult.fromJson(Map<String, dynamic> json) {
    return ATSResult(
      totalScore: json['total_score'] ?? 0,
      grade: json['grade'] ?? '',
      detailedFeedback: json['detailed_feedback'] ?? {},
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_score': totalScore,
      'grade': grade,
      'detailed_feedback': detailedFeedback,
    };
  }
}
