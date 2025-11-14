import 'package:flutter/material.dart';
import 'analyze_screen.dart';
import 'guide_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resume ATS Analyzer'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 40),
              
              // Welcome Title
              Text(
                'What would you like to do today?',
                style: Theme.of(context).textTheme.displayMedium,
                textAlign: TextAlign.center,
              ),
              
              const SizedBox(height: 40),
              
              // Feature Cards
              Expanded(
                child: ListView(
                  children: [
                    _FeatureCard(
                      icon: Icons.analytics_outlined,
                      title: 'Analyze Resume',
                      description: 'Upload your resume and get:',
                      features: const [
                        'ATS Score (0-100)',
                        'Detailed feedback on each section',
                        'Improvement suggestions',
                        'Keyword analysis',
                        'Format compatibility check',
                      ],
                      color: Colors.blue,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const AnalyzeScreen(),
                          ),
                        );
                      },
                    ),
                    
                    const SizedBox(height: 16),
                    
                    _FeatureCard(
                      icon: Icons.school_outlined,
                      title: 'Resume Guide',
                      description: 'Get expert guidance on:',
                      features: const [
                        'Creating ATS-friendly resumes',
                        'Industry-specific keywords',
                        'HR perspective insights',
                        'Common mistakes to avoid',
                        'Formatting best practices',
                      ],
                      color: Colors.purple,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const GuideScreen(),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final List<String> features;
  final Color color;
  final VoidCallback onTap;

  const _FeatureCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.features,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(icon, color: color, size: 32),
                  const SizedBox(width: 12),
                  Text(
                    title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                description,
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 12),
              ...features.map((feature) => Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('• ', style: TextStyle(color: color)),
                    Expanded(
                      child: Text(
                        feature,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                  ],
                ),
              )),
            ],
          ),
        ),
      ),
    );
  }
}
