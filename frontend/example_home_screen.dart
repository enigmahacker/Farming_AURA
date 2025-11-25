// Example Flutter Screen for Home Dashboard
// This demonstrates the UI/UX plan and API integration

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final String apiUrl = "http://localhost:8000/api";
  
  Map<String, dynamic> weather = {};
  List<Map<String, dynamic>> recommendations = [];
  String advice = "कृपया अपडेट के लिए प्रतीक्षा करें...";
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      // Fetch crop recommendations
      final recResponse = await http.post(
        Uri.parse('$apiUrl/recommendations'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'state': 'UP',
          'district': 'Lucknow',
          'soil_type': 'loam',
          'season': 'rabi',
        }),
      );

      if (recResponse.statusCode == 200) {
        recommendations =
            List<Map<String, dynamic>>.from(jsonDecode(recResponse.body));
      }

      // Fetch assistant advice
      final assistantResponse = await http.post(
        Uri.parse('$apiUrl/assistant'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': 'आज मेरे खेत के लिए क्या सलाह है?',
        }),
      );

      if (assistantResponse.statusCode == 200) {
        var data = jsonDecode(assistantResponse.body);
        advice = data['reply'] ?? 'कोई सलाह उपलब्ध नहीं है';
      }

      setState(() {
        isLoading = false;
        // Example weather data (in production, fetch from API)
        weather = {
          'temp': '28',
          'humidity': '65',
          'rain_prob': '45',
          'condition': 'आंशिक बादल',
        };
      });
    } catch (e) {
      setState(() {
        isLoading = false;
        advice = 'त्रुटि: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Farming_AURA'),
        backgroundColor: Color(0xFF2D5016), // Dark green
      ),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Weather Summary Card
                    Card(
                      elevation: 4,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            Text(
                              'आज का मौसम',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 12),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Column(
                                  children: [
                                    Icon(Icons.thermostat,
                                        size: 32, color: Colors.orange),
                                    SizedBox(height: 4),
                                    Text('${weather['temp']}°C'),
                                  ],
                                ),
                                Column(
                                  children: [
                                    Icon(Icons.water_drop,
                                        size: 32, color: Colors.blue),
                                    SizedBox(height: 4),
                                    Text('${weather['humidity']}%'),
                                  ],
                                ),
                                Column(
                                  children: [
                                    Icon(Icons.cloud_queue,
                                        size: 32, color: Colors.grey),
                                    SizedBox(height: 4),
                                    Text('${weather['rain_prob']}% वर्षा'),
                                  ],
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 16),

                    // Today's Advice Card
                    Card(
                      color: Color(0xFFF0F7E8), // Light green
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'आज की सलाह',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF2D5016),
                              ),
                            ),
                            SizedBox(height: 8),
                            Text(
                              advice,
                              style: TextStyle(fontSize: 14, height: 1.5),
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 20),

                    // Quick Actions
                    Text(
                      'त्वरित कार्य',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 12),
                    GridView.count(
                      crossAxisCount: 2,
                      shrinkWrap: true,
                      physics: NeverScrollableScrollPhysics(),
                      crossAxisSpacing: 12,
                      mainAxisSpacing: 12,
                      children: [
                        QuickActionButton(
                          icon: Icons.agriculture,
                          label: 'फसल सुझाव',
                          color: Colors.green,
                        ),
                        QuickActionButton(
                          icon: Icons.water,
                          label: 'सिंचाई अनुसूची',
                          color: Colors.blue,
                        ),
                        QuickActionButton(
                          icon: Icons.cloud,
                          label: 'मौसम पूर्वानुमान',
                          color: Colors.cyan,
                        ),
                        QuickActionButton(
                          icon: Icons.notifications,
                          label: 'सतर्कताएं',
                          color: Colors.red,
                        ),
                      ],
                    ),
                    SizedBox(height: 20),

                    // Top Crop Recommendations
                    if (recommendations.isNotEmpty)
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'अनुशंसित फसलें',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 12),
                          ...recommendations.take(3).map((crop) {
                            return Card(
                              margin: EdgeInsets.only(bottom: 12),
                              child: ListTile(
                                leading: Icon(Icons.grass_2,
                                    color: Colors.green, size: 32),
                                title: Text(crop['crop']),
                                subtitle: Text(
                                    'उपयुक्तता: ${crop['suitability_score']}/5'),
                                trailing: Icon(Icons.arrow_forward),
                              ),
                            );
                          }).toList(),
                        ],
                      ),
                  ],
                ),
              ),
            ),
    );
  }
}

class QuickActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;

  const QuickActionButton({
    required this.icon,
    required this.label,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        // Navigate to respective screen
      },
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: color),
            SizedBox(height: 8),
            Text(
              label,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  runApp(
    MaterialApp(
      title: 'Farming_AURA',
      theme: ThemeData(
        primaryColor: Color(0xFF2D5016),
        fontFamily: 'Roboto',
        useMaterial3: true,
      ),
      home: HomeScreen(),
    ),
  );
}
