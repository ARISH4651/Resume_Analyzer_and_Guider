class ApiConfig {
  // Base URL - Change this to your FastAPI server URL
  static const String baseUrl = 'http://localhost:8000';
  
  // Endpoints
  static const String parseResume = '/api/parse-resume';
  static const String calculateATS = '/api/calculate-ats';
  static const String askQuestion = '/api/ask-question';
  static const String enhanceResume = '/api/enhance-resume';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 60);
  static const Duration sendTimeout = Duration(seconds: 30);
}
