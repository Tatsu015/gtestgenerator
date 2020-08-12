#include "lefttorighttreelayoutproxy.h"
#include "utility/systemconfig.h"
#include "viewmodel/graphicsitem/connection.h"
#include "viewmodel/graphicsitem/node.h"
#include <QDebug>
#include <QRectF>

const QPointF OFFSET(10, 0);
const QPointF CUBIC_POINT(10, 0);

const QString LeftToRightTreeLayoutProxy::NAME = "Left To Right";

LeftToRightTreeLayoutProxy::LeftToRightTreeLayoutProxy() : AbstractLayoutProxy() {
}

LeftToRightTreeLayoutProxy::~LeftToRightTreeLayoutProxy() {
}

void LeftToRightTreeLayoutProxy::layout(Node* rootNode) {
  if (rootNode) {
    layoutChild(rootNode);
  }
}

QString LeftToRightTreeLayoutProxy::name() const {
  return NAME;
}

qreal LeftToRightTreeLayoutProxy::layoutChild(const Node* node) {
  const QRectF br = node->boundingRect();
  if (!node->hasChild()) {
    return br.height();
  }
  const qreal x = br.right() + systemConfig(SystemConfig::leftToRightTreeLayoutNodeXSpace).toReal();
  const qreal childHeight = childrenHeight(node);
  qreal y = br.center().y() - childHeight / 2;
  foreach (Node* childNode, node->childNodes()) {
    const qreal th = layoutChild(childNode);
    childNode->setPos(x, y + th / 2 - childNode->boundingRect().center().y());
    y += th + systemConfig(SystemConfig::leftToRightTreeLayoutNodeYSpace).toReal();
    drawConnection(node, childNode);
  }
  return qMax(childHeight, br.height());
}

qreal LeftToRightTreeLayoutProxy::treeHeight(const Node* node) {
  return qMax(childrenHeight(node), node->boundingRect().height());
}

qreal LeftToRightTreeLayoutProxy::childrenHeight(const Node* node) {
  if (!node->hasChild()) {
    return 0;
  }
  qreal leftToRightLayoutNodeYSpace = systemConfig(SystemConfig::leftToRightTreeLayoutNodeYSpace).toReal();
  qreal height = -leftToRightLayoutNodeYSpace;
  foreach (Node* childNode, node->childNodes()) {
    height += treeHeight(childNode);
    height += leftToRightLayoutNodeYSpace;
  }
  return height;
}

void LeftToRightTreeLayoutProxy::drawConnection(const Node* parentNode, const Node* childNode) {
  QPointF parentToChild = parentNode->scenePos() - childNode->scenePos();
  QPointF parentPos = parentToChild + parentNode->rightCenter() + OFFSET;
  QPointF childPos = childNode->leftCenter() - OFFSET;
  childNode->connection()->draw(parentPos, childPos, CUBIC_POINT);
}
