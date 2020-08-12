#include "scene.h"
#include "model/document.h"
#include "utility/systemconfig.h"
#include "viewmodel/graphicsitem/node.h"
#include "viewmodel/parser/markdownparser.h"
#include "viewmodel/scene/layoutproxy/abstractlayoutproxy.h"
#include "viewmodel/scene/layoutproxy/bothsidestreelayoutproxy.h"
#include "viewmodel/scene/layoutproxy/lefttorighttreelayoutproxy.h"
#include "viewmodel/scene/layoutproxy/toptobottomtreelayoutproxy.h"
#include <QTimer>

Scene::Scene(Document* document) : QGraphicsScene(), m_document(document) {
  addLayouterDecorator(new LeftToRightTreeLayoutProxy());
  addLayouterDecorator(new TopToBottomTreeLayoutProxy());
  addLayouterDecorator(new BothSidesTreeLayoutProxy());

  m_timer = new QTimer();
  connect(m_document, &Document::contentsChanged, this, &Scene::onStartTimer);
  connect(m_timer, &QTimer::timeout, this, &Scene::onUpdateMindMap);
}

Scene::~Scene() {
  qDeleteAll(m_layoutProxies);
  delete m_timer;
}

void Scene::updateMindMap() {
  MarkdownParser parser;
  m_rootNode = parser.parse(m_document->toPlainText());

  if (!m_rootNode) {
    return;
  }

  m_activeLayoutProxy->layout(m_rootNode);
  clear();
  addItem(m_rootNode);
}

void Scene::addLayouterDecorator(AbstractLayoutProxy* layoutDecolator) {
  m_layoutProxies[layoutDecolator->name()] = layoutDecolator;
}

void Scene::changeActiveLayoutDecolator(const QString& name) {
  m_activeLayoutProxy = m_layoutProxies[name];
  updateMindMap();
}

void Scene::onStartTimer() {
  m_timer->stop();
  m_timer->start(systemConfig(SystemConfig::graphicsUpdateDelayTime).toInt());
}

void Scene::onUpdateMindMap() {
  updateMindMap();
  m_timer->stop();
}

Node* Scene::rootNode() const {
  return m_rootNode;
}
