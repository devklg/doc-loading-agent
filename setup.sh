#!/bin/bash

# Documentation Loading Agent - Setup & Deployment Script
# Universal Memory Bridge

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  DOCUMENTATION LOADING AGENT - UNIVERSAL MEMORY BRIDGE         ║"
echo "║  Matrix Style Knowledge Loading                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        print_info "Install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker found"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        print_info "Install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose found"
}

# Create .env file if it doesn't exist
setup_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found, creating from template..."
        cp .env.example .env
        print_info "Please edit .env and add your Context7 API key"
        print_info "Run: nano .env"
        return 1
    else
        print_success ".env file found"
        return 0
    fi
}

# Create data directory
create_data_dir() {
    mkdir -p data
    print_success "Data directory created"
}

# Build Docker images
build_images() {
    print_info "Building Docker images..."
    docker-compose build
    print_success "Images built successfully"
}

# Start services
start_services() {
    print_info "Starting services..."
    docker-compose up -d
    print_success "Services started"
    
    # Wait for ChromaDB to be ready
    print_info "Waiting for ChromaDB to be ready..."
    sleep 5
    
    if docker-compose ps | grep -q "chromadb.*Up"; then
        print_success "ChromaDB is running"
    else
        print_error "ChromaDB failed to start"
        docker-compose logs chromadb
        exit 1
    fi
}

# Stop services
stop_services() {
    print_info "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Load documentation
load_docs() {
    print_info "Loading framework documentation..."
    docker-compose exec -T doc_loader python load_frameworks.py load
    print_success "Documentation loaded"
}

# Load priority documentation only
load_priority() {
    print_info "Loading priority frameworks..."
    docker-compose exec -T doc_loader python load_frameworks.py load --priority
    print_success "Priority documentation loaded"
}

# Verify documentation
verify_docs() {
    print_info "Verifying documentation..."
    docker-compose exec -T doc_loader python load_frameworks.py verify
}

# Create index
create_index() {
    print_info "Creating documentation index..."
    docker-compose exec -T doc_loader python load_frameworks.py index
    print_success "Index created"
}

# Show status
show_status() {
    echo ""
    print_info "Service Status:"
    docker-compose ps
    echo ""
    
    if [ -f data/documentation_index.json ]; then
        print_info "Documentation Index:"
        cat data/documentation_index.json | jq -r '.total_frameworks, .total_documents'
    fi
}

# Show logs
show_logs() {
    docker-compose logs -f
}

# Backup ChromaDB
backup_chromadb() {
    BACKUP_DIR="backups/chromadb_$(date +%Y%m%d_%H%M%S)"
    print_info "Backing up ChromaDB to $BACKUP_DIR..."
    mkdir -p $BACKUP_DIR
    docker cp chromadb:/chroma/chroma $BACKUP_DIR/
    print_success "Backup completed: $BACKUP_DIR"
}

# Main menu
show_menu() {
    echo ""
    echo "Commands:"
    echo "  setup         - Initial setup (check dependencies, create .env)"
    echo "  start         - Start services"
    echo "  stop          - Stop services"
    echo "  restart       - Restart services"
    echo "  load          - Load all documentation"
    echo "  load-priority - Load priority documentation only"
    echo "  verify        - Verify documentation"
    echo "  index         - Create documentation index"
    echo "  status        - Show service status"
    echo "  logs          - Show logs"
    echo "  backup        - Backup ChromaDB"
    echo "  clean         - Stop and remove all data (WARNING!)"
    echo ""
}

# Main script logic
case "${1:-}" in
    setup)
        print_info "Running initial setup..."
        check_docker
        check_docker_compose
        create_data_dir
        setup_env || exit 1
        build_images
        print_success "Setup complete!"
        print_info "Next steps:"
        print_info "  1. Edit .env and add your Context7 API key"
        print_info "  2. Run: ./setup.sh start"
        print_info "  3. Run: ./setup.sh load"
        ;;
    
    start)
        start_services
        show_status
        ;;
    
    stop)
        stop_services
        ;;
    
    restart)
        stop_services
        start_services
        show_status
        ;;
    
    load)
        load_docs
        create_index
        verify_docs
        ;;
    
    load-priority)
        load_priority
        create_index
        verify_docs
        ;;
    
    verify)
        verify_docs
        ;;
    
    index)
        create_index
        ;;
    
    status)
        show_status
        ;;
    
    logs)
        show_logs
        ;;
    
    backup)
        backup_chromadb
        ;;
    
    clean)
        print_warning "This will stop services and remove all data!"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            docker-compose down -v
            rm -rf data/*
            print_success "Cleaned up"
        else
            print_info "Cancelled"
        fi
        ;;
    
    *)
        show_menu
        print_error "Please specify a command"
        exit 1
        ;;
esac
