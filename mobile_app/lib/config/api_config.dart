class ApiConfig {
  // Base URL - Change this to your FastAPI server URL
  // Use localhost for same machine, or your computer's IP for other devices on WiFi
  static const String baseUrl = 'http://192.168.0.3:8000';  // PC IP address for WiFi access
  
  // Endpoints
  static const String parseResume = '/api/parse-resume';
  static const String calculateATS = '/api/calculate-ats';
  static const String askQuestion = '/api/ask-question';
  static const String enhanceResume = '/api/enhance-resume';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 120);
  static const Duration receiveTimeout = Duration(seconds: 300);
  static const Duration sendTimeout = Duration(seconds: 120);
}
