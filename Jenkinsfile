pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        dockerfile {
          filename 'Dockerfile'
          label 'service-agent'
          args '--network internal'
        }
      }
      environment {
        REDIS_HOST = 'redis'
      }
      steps {
        sh 'cd /app && pytest doku/tests --junitxml=$WORKSPACE/TESTS.xml'
        junit 'TESTS.xml'
      }
    }
    stage('Build') {
      when {
        beforeAgent true
        anyOf {
          branch 'main'
        }
      }
      agent {
        label 'service-agent'
      }
      environment {
        REGISTRY = credentials('desklab-registry')
      }
      steps {
        sh 'docker build -t reg.desk-lab.de/doku -t reg.desk-lab.de/doku:$GIT_COMMIT .'
        sh 'cd doku/static && docker build -t reg.desk-lab.de/doku-static -t reg.desk-lab.de/doku-static:$GIT_COMMIT .'
        sh 'docker login https://reg.desk-lab.de --username $REGISTRY_USR --password $REGISTRY_PSW'
        sh 'docker push reg.desk-lab.de/doku-static | cat'
        sh 'docker push reg.desk-lab.de/doku-static:$GIT_COMMIT | cat'
        sh 'docker push reg.desk-lab.de/doku | cat'
        sh 'docker push reg.desk-lab.de/doku:$GIT_COMMIT | cat'
      }
    }
    stage('Deploy') {
      when {
        beforeAgent true
        anyOf {
          branch 'main'
        }
      }
      agent {
        label 'deploy-agent'
      }
      options { skipDefaultCheckout() }
      environment {
        REGISTRY = credentials('desklab-registry')
      }
      steps {
        sh 'docker login https://reg.desk-lab.de --username $REGISTRY_USR --password $REGISTRY_PSW'
        sh 'cd /home/jenkins/server && docker-compose pull doku dokustatic | cat'
        sh 'cd /home/jenkins/server && docker-compose up -d doku dokustatic | cat'
      }
    }
  }
}
