import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import '../services/api_service.dart';
import '../models/ats_result.dart';
import 'result_screen.dart';

class AnalyzeScreen extends ConsumerStatefulWidget {
  const AnalyzeScreen({super.key});

  @override
  ConsumerState<AnalyzeScreen> createState() => _AnalyzeScreenState();
}

class _AnalyzeScreenState extends ConsumerState<AnalyzeScreen> {
  final TextEditingController _jobDescController = TextEditingController();
  String? _fileName;
  String? _filePath;
  bool _isAnalyzing = false;

  @override
  void dispose() {
    _jobDescController.dispose();
    super.dispose();
  }

  Future<void> _pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'docx'],
    );

    if (result != null) {
      setState(() {
        _fileName = result.files.single.name;
        _filePath = result.files.single.path;
      });
    }
  }

  Future<void> _analyzeResume() async {
    if (_filePath == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a resume first')),
      );
      return;
    }

    setState(() => _isAnalyzing = true);

    try {
      final apiService = ref.read(apiServiceProvider);
      
      // Parse resume
      final parsed = await apiService.parseResume(_filePath!);
      
      // Calculate ATS score
      final atsResult = await apiService.calculateATSScore(
        parsed,
        _jobDescController.text.trim(),
      );

      if (!mounted) return;

      // Navigate to result screen
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultScreen(
            atsResult: atsResult,
            parsedResume: parsed,
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      setState(() => _isAnalyzing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analyze Resume'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Job Description (Optional)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Job Description (Optional)',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Add job description for better keyword matching',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        controller: _jobDescController,
                        maxLines: 5,
                        decoration: const InputDecoration(
                          hintText: 'Paste job description here...',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 24),
              
              // File Upload Section
              Card(
                child: InkWell(
                  onTap: _pickFile,
                  borderRadius: BorderRadius.circular(12),
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      children: [
                        Icon(
                          _fileName == null
                              ? Icons.upload_file_outlined
                              : Icons.check_circle_outline,
                          size: 64,
                          color: _fileName == null
                              ? Colors.grey
                              : Colors.green,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          _fileName ?? 'Upload Resume',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _fileName == null
                              ? 'PDF or DOCX format'
                              : 'Tap to change file',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              
              const SizedBox(height: 24),
              
              // Analyze Button
              ElevatedButton(
                onPressed: _isAnalyzing ? null : _analyzeResume,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: _isAnalyzing
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      )
                    : const Text(
                        'Analyze Resume',
                        style: TextStyle(fontSize: 16),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
