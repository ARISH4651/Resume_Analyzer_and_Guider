import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/api_config.dart';
import '../models/ats_result.dart';

final apiServiceProvider = Provider((ref) => ApiService());

class ApiService {
  late final Dio _dio;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: ApiConfig.connectTimeout,
      receiveTimeout: ApiConfig.receiveTimeout,
      sendTimeout: ApiConfig.sendTimeout,
      headers: {
        'Content-Type': 'application/json',
      },
    ));
  }

  // Parse Resume
  Future<Map<String, dynamic>> parseResume(String filePath) async {
    try {
      FormData formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(filePath),
      });

      final response = await _dio.post(
        ApiConfig.parseResume,
        data: formData,
      );

      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Calculate ATS Score
  Future<ATSResult> calculateATSScore(
    Map<String, dynamic> parsedResume,
    String jobDescription,
  ) async {
    try {
      final response = await _dio.post(
        ApiConfig.calculateATS,
        data: {
          'parsed_resume': parsedResume,
          'job_description': jobDescription,
        },
      );

      return ATSResult.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Ask Question (RAG)
  Future<String> askQuestion(String question) async {
    try {
      final response = await _dio.post(
        ApiConfig.askQuestion,
        data: {'question': question},
      );

      return response.data['answer'];
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Enhance Resume
  Future<Map<String, dynamic>> enhanceResume(
    Map<String, dynamic> parsedResume,
  ) async {
    try {
      final response = await _dio.post(
        ApiConfig.enhanceResume,
        data: {'parsed_resume': parsedResume},
      );

      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException e) {
    if (e.response != null) {
      return e.response?.data['detail'] ?? 'Server error occurred';
    } else {
      return 'Network error: ${e.message}';
    }
  }
}
